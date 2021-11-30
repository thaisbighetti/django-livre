import http
from django.db import transaction
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Client, Transfer, Account
from .serializers import TransferSerializer, AccountSerializer, ClientSerializer


class MainPage(APIView):
    http_method_names = ['get']

    def get(self, request):
        urls = {'Create User': 'create-user/',
                'User Detail': 'user/<str:cpf>/',
                'All Users': 'all-users/',
                'Bank Transfer': 'transfer/',
                'All Transfers': 'all-transfers/',
                'All User Transfers Received': 'transfers-received/<str:cpf>/',
                'All User Transfers Performed': 'transfers-performed/<str:cpf>/',
                'Bank Account': 'account/<str:id>/',
                'All Bank Accounts': 'all-accounts',
                }

        return Response(urls, status=http.HTTPStatus.OK)


class CreateUser(APIView):
    serializer_class = ClientSerializer
    http_method_names = ['get', 'post', ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                account = Account.objects.create(account_user_id=request.data['cpf'], )
                account.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserView(generics.ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def list(self, request):
        users = self.get_queryset()
        serializer = ClientSerializer(users, many=True)
        return Response(serializer.data)


class UserSearch(generics.ListAPIView):
    serializer_class = ClientSerializer

    def list(self, request, cpf):
        user = Client.objects.get(cpf=cpf)
        serializer = ClientSerializer(user)
        return Response(serializer.data, status=http.HTTPStatus.OK)

    def put(self, request, cpf):
        user = Client.objects.get(cpf=cpf)
        serializer = ClientSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
        return Response(serializer.data, status=http.HTTPStatus.OK)


class CreateTransfer(APIView):
    serializer_class = TransferSerializer
    http_method_names = ['get', 'post', ]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if request.data['source_cpf'] != ['target_cpf']:
                source_user = Account.objects.get(account_user=request.data['source_cpf'])
                target_user = Account.objects.get(account_user=request.data['target_cpf'])
                if (float(request.data['value']) > source_user.balance) or (source_user == target_user):
                    return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    source_user.balance = source_user.balance - float(request.data['value'])
                    target_user.balance = target_user.balance + float(request.data['value'])
                    with transaction.atomic():
                        target_user.save()
                        source_user.save()
                        serializer.save()
                    return Response({"Transferência realizada": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TransfersView(generics.ListAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer


class TransfersPerformed(APIView):
    http_method_names = ['get', ]
    serializer_class = TransferSerializer

    def get(self, request, cpf):
        transferencias = Transfer.objects.filter(source_cpf=cpf)
        serializer = TransferSerializer(transferencias, many=True)
        return Response({"Histórico de transferências realizadas pelo usuário": serializer.data},
                        status=status.HTTP_200_OK)


class TransfersReceived(APIView):
    http_method_names = ['get', ]
    serializer_class = TransferSerializer

    def get(self, request, cpf):
        transfers = Transfer.objects.filter(target_cpf=cpf)
        serializer = TransferSerializer(transfers, many=True)
        return Response({"Histórico de transferências recebidas pelo usuário": serializer.data},
                        status=status.HTTP_200_OK)


class AccountsView(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountView(APIView):
    http_method_names = ['get', ]
    serializer_class = AccountSerializer

    def get(self, request, cpf):
        user = Account.objects.get(account_user=cpf)
        serializer = AccountSerializer(user)
        return Response(serializer.data)
