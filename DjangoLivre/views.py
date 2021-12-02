import http
from django.db import transaction
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Client, Transfer, Account
from .serializers import TransferSerializer, AccountSerializer, ClientSerializer


class MainPage(APIView):
    http_method_names = ['get']
    """
    Description of routes according to the desired action
    Each route will be detailed in the urls.py layer
    """

    def get(self, request):
        urls = {'Create User': 'create-user/',
                'User Detail': 'user/<str:cpf>/',
                'All Users': 'all-users/',
                'Bank Transfer': 'transfer/',
                'All Transfers': 'all-transfers/',
                'All User Transfers Received': 'transfers-received/<str:cpf>/',
                'All User Transfers Performed': 'transfers-performed/<str:cpf>/',
                'Bank Account': 'account/<str:cpf>/',
                'All Bank Accounts': 'all-accounts',
                }
        return Response(urls, status=http.HTTPStatus.OK)


class CreateUser(APIView):
    serializer_class = ClientSerializer
    http_method_names = ['get', 'post', ]
    """
    Create a user and present what was created
    """

    def post(self, request):
        """
        It expects:
            - POST as http method;
            - url/create-user/

        It returns:
             - HTTP status = 200;
             - A JSON like this:
                {
                    "cpf": "48748589292",
                    "name": "Maria",
                    "phone": "+5511912345678",
                    "email": "maria@gmail.com",
                    "creation": "2021-12-01T01:19:59.465753Z"
                }
            - GET as http method;
             """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if request.data['cpf'].isalnum():
                with transaction.atomic():
                    serializer.save()
                    account = Account.objects.create(account_user_id=request.data['cpf'], )
                    account.save()
                return Response({'Usuário Cadastrado': serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'Erro': "O CPF deve ser sem ponto e traço"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    """
    Lists registered users.
    """

    def list(self, request):
        """
        It expects:
            - GET as http method;
            - url/all-users/
        It returns:
            - HTTP status = 200;
            - A JSON like this:
                [
                    {
                        "cpf": "48748589292",
                        "name": "Maria",
                        "phone": "+5511912345678",
                        "email": "maria@gmail.com",
                        "creation": "2021-12-01T01:19:59.465753Z"
                    },
                    {
                        "cpf": "10955470625",
                        "name": "Fabia",
                        "phone": "+5511912345678",
                        "email": "fabia@hotmail.com",
                        "creation": "2021-12-01T01:24:58.720956Z"
                    }
                ]
        """
        users = self.get_queryset()
        serializer = ClientSerializer(users, many=True)
        return Response(serializer.data)


class UserSearch(generics.ListAPIView):
    serializer_class = ClientSerializer
    """
    Gets and/or change the data of a specific user.
    """

    def list(self, request, cpf):
        """
        It expects:
            - GET as http method;
            - The ID-CPF, specified on the url;
            - url/user/cpf
        It returns:
            - HTTP status = 200;
            - A JSON like this:
                {
                    "cpf": "97417972144",
                    "name": "José",
                    "phone": "+5511912345678",
                    "email": "jose@gmail.com",
                    "creation": "2021-12-01T18:05:29.214828Z"
                }
        """
        user = Client.objects.get(cpf=cpf)
        serializer = ClientSerializer(user)
        return Response(serializer.data, status=http.HTTPStatus.OK)

    def put(self, request, cpf):
        """
        PUT as http method;
        - Save the changes made for the requested user
        """
        user = Client.objects.get(cpf=cpf)
        serializer = ClientSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
        return Response({'Usuário atualizado:': serializer.data}, status=http.HTTPStatus.OK)

    def delete(self, request, cpf):
        """
        DELETE as http method;
        - Deletes the requested user
        """
        user = Client.objects.get(cpf=cpf)
        user.delete()
        return Response(status=http.HTTPStatus.NO_CONTENT)


class CreateTransfer(APIView):
    serializer_class = TransferSerializer
    http_method_names = ['get', 'post', ]
    """
    Create a transfer and present what was created
    """

    def post(self, request):
        """
        Posts the new transfer:
            It expects:
                - POST as http method;
                - url/transfer/;
                - Requires already registered source cpf and destination cpf

            It returns:
                - HTTP status = 200;
                - A JSON like this:
                 {
                    "Transferência realizada":
                        {
                            "id": 1,
                            "source_cpf": "97417972144",
                            "target_cpf": "109.554.706-25",
                            "value": 50.0,
                            "date": "2021-12-01T18:58:39.564256Z"
                        }
                }

        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if request.data['source_cpf'] != ['target_cpf']:
                source_user = Account.objects.get(account_user=request.data['source_cpf'])
                target_user = Account.objects.get(account_user=request.data['target_cpf'])
                if float(request.data['value']) > source_user.balance:
                    return Response(
                        {"status": "O saldo da conta de origem deve ser maior que o valor da transferência"},
                        status=status.HTTP_400_BAD_REQUEST)
                elif source_user == target_user:
                    return Response({"error": "Os usuários de destino e origem devem ser diferentes"},
                                    status=status.HTTP_400_BAD_REQUEST)
                else:
                    source_user.balance = source_user.balance - float(request.data['value'])
                    target_user.balance = target_user.balance + float(request.data['value'])
                    with transaction.atomic():
                        target_user.save()
                        source_user.save()
                        serializer.save()
                    return Response({"Transferência realizada": serializer.data}, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response({"error:": "Confira os dados informados"}, status=status.HTTP_400_BAD_REQUEST)


class TransfersView(generics.ListAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    """
    Lists registered transfers.
    It expects:
        - GET as http method;
        - url/all-transfers/
    It returns:
        - HTTP status = 200;
        - A JSON like this:
            [
                {
                    "id": 1,
                    "source_cpf": "97417972144",
                    "target_cpf": "10955470625",
                    "value": 50.0,
                    "date": "2021-12-01T18:58:39.564256Z"
                },
                {
                    "id": 2,
                    "source_cpf": "10955470625",
                    "target_cpf": "97417972144",
                    "value": 50.0,
                    "date": "2021-12-01T19:16:05.125610Z"
                }
            ]
    """


class TransfersPerformed(APIView):
    http_method_names = ['get', ]
    serializer_class = TransferSerializer
    """
    Lists transfers performed by a specific user.
    """

    def get(self, request, cpf):
        """
        It expects:
            - GET as http method;
            - The ID-CPF, specified on the url;
            - url/transfers-performed/cpf
        It returns:
            - HTTP status = 200;
            - A JSON like this:
                {
                        "Histórico de transferências realizadas pelo usuário":
                    [
                        {
                            "id": 1,
                            "source_cpf": "97417972144",
                            "target_cpf": "10955470625",
                            "value": 50.0,
                            "date": "2021-12-01T18:58:39.564256Z"
                        }
                    ]
                }

        """

        transferencias = Transfer.objects.filter(source_cpf=cpf)
        serializer = TransferSerializer(transferencias, many=True)
        return Response({"Histórico de transferências realizadas pelo usuário": serializer.data},
                        status=status.HTTP_200_OK)


class TransfersReceived(APIView):
    http_method_names = ['get', ]
    serializer_class = TransferSerializer
    """
    Lists transfers received by a specific user.
    """

    def get(self, request, cpf):
        """
        It expects:
            - GET as http method;
            - The ID-CPF, specified on the url;
            - url/transfers-received/cpf
        It returns:
            - HTTP status = 200;
            - A JSON like this:
                {
                    "Histórico de transferências recebidas pelo usuário":
                    [
                        {
                            "id": 2,
                            "source_cpf": "10955470625",
                            "target_cpf": "97417972144",
                            "value": 50.0,
                            "date": "2021-12-01T19:16:05.125610Z"
                        }
                    ]
                }
        """

        transfers = Transfer.objects.filter(target_cpf=cpf)
        serializer = TransferSerializer(transfers, many=True)
        return Response({"Histórico de transferências recebidas pelo usuário": serializer.data},
                        status=status.HTTP_200_OK)


class AccountsView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    """
    List all registered accounts
    
     It expects:
        - GET as http method;
        - url/all-accounts/
     It returns:
        - HTTP status = 200;
        - A JSON like this:
            [
                 {
                    "account_user": "109.554.706-25",
                    "number": "97f33114-5b31-4d09-b651-3d6e3f5b38ad",
                    "balance": 5000
                 },
                {
                    "account_user": "97417972144",
                    "number": "e0d3a06b-18f1-4ff9-b9bf-831ad4701edd",
                    "balance": 5000
                }
            ]
    """



class AccountView(APIView):
    http_method_names = ['get', ]
    serializer_class = AccountSerializer
    """
    Return the account of a specific user
    """

    def get(self, request, cpf):
        """
        It expects:
            - GET as http method;
            - The ID-CPF, specified on the url;
            - url/account/cpf
        It returns:
            - HTTP status = 200;
            - A JSON like this:
                {
                    "account_user": "97417972144",
                    "number": "e0d3a06b-18f1-4ff9-b9bf-831ad4701edd",
                    "balance": 5000
                }
        """
        user = Account.objects.get(account_user=cpf)
        serializer = AccountSerializer(user)
        return Response(serializer.data)
