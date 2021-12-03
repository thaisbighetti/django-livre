from datetime import datetime
from unittest.mock import ANY
from django.http.response import JsonResponse
from django.test import TestCase
from rest_framework.test import RequestsClient

from .models import Client, Transfer, Account
from .test_utils import generate_valid_cpf, post_two_clients

class APIEndpointsTest(TestCase):
    """
    Testing if our endpoint methods are working properly, by giving them 
    valid data and analysing the responses.
    """
    
    @classmethod
    def setUpTestData(cls): # setting up data for all tests in class
        cls.cliente_1 = Client.objects.create(
            name = 'name_1', cpf = 'cpf_1',
            email = 'name_1@gmail.com',
            phone = '11987654321'
        )
        cls.cliente_2 = Client.objects.create(
            name = 'name_2', cpf = 'cpf_2',
            email = 'name_2@gmail.com',
            phone = '21987654321'
        )

    def setUp(self):
        """
        Initializing our API client to test our http methods
        """
        self.client = RequestsClient()

    def test_should_get_main_page_with_http_200(self):
        """
        Testing if the main page's response is 200 - OK (MainPage view)
        """
        response = self.client.get('http://127.0.0.1:8000')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'Create User': 'create-user/',
                'User Detail': 'user/<str:cpf>/',
                'All Users': 'all-users/',
                'Bank Transfer': 'transfer/',
                'All Transfers': 'all-transfers/',
                'All User Transfers Received': 'transfers-received/<str:cpf>/',
                'All User Transfers Performed': 'transfers-performed/<str:cpf>/',
                'Bank Account': 'account/<str:cpf>/',
                'All Bank Accounts': 'all-accounts',
                })
    
    def test_should_get_all_clients_with_http_200(self):
        """
        Testing if the clients created with setUpTestData are retrieved
        with GET method on endpoint 'all-users/' (UserView view)
        """
        response = self.client.get('http://127.0.0.1:8000/all-users/')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response,
            [{'cpf': 'cpf_1', 'name': 'name_1', 
            'phone': '+5511987654321', 'email': 'name_1@gmail.com', 
            'creation': ANY}, 
            {'cpf': 'cpf_2', 'name': 'name_2', 'phone': '+5521987654321', 
            'email': 'name_2@gmail.com', 'creation': ANY}])

    def test_should_search_client_cpf_with_http_200(self):
        """
        Testing if the users can be searched, by
        their cpf on endpoint 'user/<str:cpf>/' (UserSearch view)
        """
        response = self.client.get('http://127.0.0.1:8000/user/cpf_1')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response, 
            {'cpf': 'cpf_1', 'name': 'name_1', 
            'phone': '+5511987654321', 'email': 'name_1@gmail.com', 
            'creation': ANY})

    def test_should_post_users_and_create_accounts(self):
        """
        Testing if posting an user creates an account associated with that user.
        Since our Client and Account classes are related, and the CreateUser view 
        creates also an account, we are testing the CreateUser view POST method,
        and if it is creating instances of Account.
        """
        self.assertEqual(Account.objects.count(), 0)
        # since we haven't POSTED the clients, no account should be registered
        client_data = {'cpf': generate_valid_cpf(), 
        'name': 'name_3', 
        'phone': '+5531987654321', 
        'email': 'name_3@gmail.com',
        'date': datetime.now() 
        }

        response = self.client.post('http://127.0.0.1:8000/create-user/', client_data)
        json_response = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response,
            {'Usuário Cadastrado': {
            'cpf': ANY, 'name': 'name_3', # since the cpf is random generated, we just check if it's there
            'phone': '+5531987654321', 'email': 'name_3@gmail.com', 
            'creation': ANY}})

        # so now we should have 3 clients (2 via create and 1 via post) but only 1 account
        self.assertEqual(Client.objects.count(), 3)
        self.assertEqual(Account.objects.count(), 1)
        # now we are sure our post method insures our client creates an account by registering

    def test_should_get_all_accounts_with_http_200(self):
        """
        Testing if the accounts created when posting the clients are retrieved
        with GET method on endpoint 'all-accounts/' (AccountsView view)
        """
        posting = post_two_clients
        posting()

        response = self.client.get('http://127.0.0.1:8000/all-accounts/')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response), 2)
        self.assertEqual(json_response,
            [{'account_user': ANY, 'number': ANY, 'balance': 5000}, 
            {'account_user': ANY, 'number': ANY, 'balance': 5000}])

    def test_should_get_accounts_by_cpf_with_http_200(self):
        """
        Testing if the accounts we create by posting a client are effectively assigned
        to their user by checking the behavior of GET method on the 'account/<str:cpf>/'
        endpoint (AccountView)
        """
        posting = post_two_clients
        posting()
        client_3 = Client.objects.get(name='name_3')
        cpf_3 = client_3.cpf

        response = self.client.get(f'http://127.0.0.1:8000/account/{cpf_3}/')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response, 
            {'account_user': ANY, 'number': ANY, 'balance': 5000})

    def test_should_create_transfer_with_http_201(self):
        """
        Testing if the 'transfer/' path can correctly create a tranfer (CreateTransfer View).
        The other responses for invalid requests will be tested in the validation classes
        """
        posting = post_two_clients
        posting()
        source_client = Client.objects.get(name='name_3')
        target_client = Client.objects.get(name='name_4')
        source_cpf = source_client.cpf
        target_cpf = target_client.cpf
    
        transfer = {
        "source_cpf": source_cpf,
        "target_cpf": target_cpf,
        "value": 10.0
        }

        response = self.client.post('http://127.0.0.1:8000/transfer/', transfer)
        json_response = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transfer.objects.count(), 1)
        self.assertEqual(json_response,
            {'Transferência realizada': {'id': 1, 'source_cpf': source_cpf, 
            'target_cpf': target_cpf, 'value': 10.0, 'date': ANY}})

    def test_should_get_transfer_with_http_200(self):
        """
        Testing if the log of posted transfers are retrieved
        with GET method on endpoint 'all-transfers/' (TransfersView)
        """
        posting = post_two_clients
        posting()
        source_client = Client.objects.get(name='name_3')
        target_client = Client.objects.get(name='name_4')
        source_cpf = source_client.cpf
        target_cpf = target_client.cpf
    
        transfer = {
        "source_cpf": source_cpf,
        "target_cpf": target_cpf,
        "value": 10.0
        }
        transfering = self.client.post('http://127.0.0.1:8000/transfer/', transfer)

        response = self.client.get('http://127.0.0.1:8000/all-transfers/')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response,
            [{'id': 1, 'source_cpf': source_cpf, 'target_cpf': target_cpf, 
            'value': 10.0, 'date': ANY}])

    def test_should_get_received_transfers_with_http_200(self):
        """
        Testing if the log of posted transfers received by a user are retrieved
        with GET method on endpoint 'transfers-received/<str:cpf>/' (TransfersReceived View))
        """
        posting = post_two_clients
        posting()
        source_client = Client.objects.get(name='name_3')
        target_client = Client.objects.get(name='name_4')
        source_cpf = source_client.cpf
        target_cpf = target_client.cpf
    
        transfer = {
        "source_cpf": source_cpf,
        "target_cpf": target_cpf,
        "value": 10.0
        }
        transfering = self.client.post('http://127.0.0.1:8000/transfer/', transfer)

        response = self.client.get(f'http://127.0.0.1:8000/transfers-received/{target_cpf}/')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response), 1)
        self.assertEqual(json_response,
            {'Histórico de transferências recebidas pelo usuário': 
            [{'id': 1, 'source_cpf': source_cpf, 'target_cpf': target_cpf, 
            'value': 10.0, 'date': ANY}]})

    def test_should_get_performed_transfers_with_http_200(self):
        """
        Testing if the log of posted transfers performed by a user are retrieved
        with GET method on endpoint 'transfers-performed/<str:cpf>/' (TransfersPerformed View))
        """
        posting = post_two_clients
        posting()
        source_client = Client.objects.get(name='name_3')
        target_client = Client.objects.get(name='name_4')
        source_cpf = source_client.cpf
        target_cpf = target_client.cpf
    
        transfer = {
        "source_cpf": source_cpf,
        "target_cpf": target_cpf,
        "value": 10.0
        }
        transfering = self.client.post('http://127.0.0.1:8000/transfer/', transfer)

        response = self.client.get(f'http://127.0.0.1:8000/transfers-performed/{source_cpf}/')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json_response), 1)
        self.assertEqual(json_response,
            {'Histórico de transferências realizadas pelo usuário': 
            [{'id': 1, 'source_cpf': source_cpf, 'target_cpf': target_cpf, 
            'value': 10.0, 'date': ANY}]})

class APIValidationsTest(TestCase):
    """
    Testing if our endpoint methods are giving the correct responses when we
    try to post invalid or incorrect data. 
    """

    def setUp(self):
        """
        Initializing our API client to test our http methods
        """
        self.client = RequestsClient()

    def test_should_not_post_user_with_http_400(self):
        """
        Testing if trying to create an user with invalid data (like invalid cpf or phone)
        returns a 400_BAD_REQUEST response on endpoint 'create-user/' (CreateUser view)
        """
        client_data = {'cpf': '11111111111', # sequences like this are invalid cpfs 
        'name': 'name_1', 
        'phone': '+5531987654321', 
        'email': 'name_2@gmail.com',
        'date': datetime.now() 
        }

        client_data_2 = {'cpf': generate_valid_cpf(),
        'name': 'name_2', 
        'phone': '987654321', # phone without local DDD
        'email': 'name_2@gmail.com',
        'date': datetime.now() 
        }        
        
        client_data_3 = {'cpf': generate_valid_cpf(),
        'name': 'name_2', 
        'phone': '987654321',
        'email': 'name_2', # invalid email
        'date': datetime.now() 
        }

        response = self.client.post('http://127.0.0.1:8000/create-user/', client_data)
        response_2 = self.client.post('http://127.0.0.1:8000/create-user/', client_data_2)
        response_3 = self.client.post('http://127.0.0.1:8000/create-user/', client_data_3)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(response_3.status_code, 400)
        self.assertEqual(Client.objects.count(), 0)
        self.assertEqual(Account.objects.count(), 0)

    def test_should_not_get_clients_with_http_200(self):
        """
        Testing if trying to get the list of users when there's none created
        returns a an empty json on endpoint 'all-users/' (UserView)
        """
        response = self.client.get('http://127.0.0.1:8000/all-users/')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response, [])

    def test_should_not_get_user_not_created_with_http_500(self):
        """
        Testing if trying to get a non-created (or posted) user
        returns a 500 response on endpoint 'user/<str:cpf>/' (UserSearch view)  
        """
        client_data = {'cpf': generate_valid_cpf(),
        'name': 'name_1', 
        'phone': '+5511987654321', 
        'email': 'name_1@gmail.com',
        'date': datetime.now() 
        }        
        another_cpf = generate_valid_cpf()

        response_post = self.client.post('http://127.0.0.1:8000/create-user/', client_data)
        response_get = self.client.get(f'http://127.0.0.1:8000/user/{another_cpf}')

        self.assertEqual(response_post.status_code, 201)
        self.assertEqual(response_get.status_code, 500)
        """
        Note: this response can be changed to 404 by using get_object_or_404 
        from django.shortcuts on the UserSearch view.
        """

    def test_should_not_get_accounts_with_200(self):
        """
        Testing if trying to get the list of accounts when there's none created
        returns an empty json on endpoint 'all-accounts/' (AccountsView)
        """
        response = self.client.get('http://127.0.0.1:8000/all-accounts/')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response, [])

    def test_should_not_get_uncreated_account_with_http_500(self):
        """
        Testing if trying to get a non-created account
        returns a 400_BAD_REQUEST response on endpoint 'account/<str:cpf>/' (AccountView)  
        """
        client_data = {'cpf': generate_valid_cpf(),
        'name': 'name_1', 
        'phone': '+5511987654321', 
        'email': 'name_1@gmail.com',
        'date': datetime.now() 
        }        
        another_cpf = generate_valid_cpf()

        response_post = self.client.post('http://127.0.0.1:8000/create-user/', client_data)
        response_get = self.client.get(f'http://127.0.0.1:8000/account/{another_cpf}')

        self.assertEqual(response_post.status_code, 201)
        self.assertEqual(response_get.status_code, 500)
        self.assertEqual(Account.objects.count(), 1)

    def test_should_not_get_transfer_not_created_with_http_200(self):
        """
        Testing if trying to get a non-created  transfer
        returns a 200 response on endpoint 'all-transfers/' (TransfersView)  
        """
        response = self.client.get('http://127.0.0.1:8000/all-transfers/')
        json_response = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response, [])

    def test_should_not_get_uncreated_transfers_with_http_200(self):
        """
        Testing if trying to get a non-created performed or received transfer
        returns a 200 response on endpoints 'transfers-performed/<str:cpf>/' (TransfersPerformed) 
        and 'transfers-received/<str:cpf>/' (TransfersReceived) 
        """
        response_performed = self.client.get('http://127.0.0.1:8000/transfers-performed/11111111111')
        json_performed = response_performed.json()        
        response_received = self.client.get('http://127.0.0.1:8000/transfers-received/11111111111')
        json_received = response_received.json()

        self.assertEqual(response_performed.status_code, 200)
        self.assertEqual(response_received.status_code, 200)
        self.assertEqual(
            json_performed,
            {'Histórico de transferências realizadas pelo usuário': []}
        )
        self.assertEqual(
            json_received,
            {'Histórico de transferências recebidas pelo usuário': []}
        )

    def test_should_not_post_transfer_with_invalid_cpf(self):
        """
        Testing if trying to pass an invalid CPF returns a 400 response on
        'transfer/' endpoint (CreateTransfer view)
        """
        transfer = {
        "source_cpf": 11111111111,
        "target_cpf": 22222222222,
        "value": 10.0
        }

        response = self.client.post('http://127.0.0.1:8000/transfer/', transfer)
        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transfer.objects.count(), 0)
        self.assertEqual(json_response,
            {'error:': 'Confira os dados informados'})

    def test_should_not_create_transfer_without_enough_money(self):
        """
        Testing if trying to transfer more than the source balance returns
        a 400 response on 'transfer/' endpoint (CreateTransfer view)
        """
        posting = post_two_clients
        posting()
        source_client = Client.objects.get(name='name_3')
        target_client = Client.objects.get(name='name_4')
        source_cpf = source_client.cpf
        target_cpf = target_client.cpf
    
        transfer = {
        "source_cpf": source_cpf,
        "target_cpf": target_cpf,
        "value": 8000.0  # the balance is 5000
        }

        response = self.client.post('http://127.0.0.1:8000/transfer/', transfer)
        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transfer.objects.count(), 0)
        self.assertEqual(json_response,
            {'status': 'O saldo da conta de origem deve ser maior que o valor da transferência'})

    def test_should_not_create_transfer_to_same_user(self):
        """
        Testing if trying to transfer to the same account returns
        a 400 response on 'transfer/' endpoint (CreateTransfer view)
        """
        posting = post_two_clients
        posting()
        source_client = Client.objects.get(name='name_3')
        target_client = Client.objects.get(name='name_4')
        source_cpf = source_client.cpf
        target_cpf = target_client.cpf
    
        transfer = {
        "source_cpf": source_cpf,
        "target_cpf": source_cpf,
        "value": 10.0  # the balance is 5000
        }

        response = self.client.post('http://127.0.0.1:8000/transfer/', transfer)
        json_response = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Transfer.objects.count(), 0)
        self.assertEqual(json_response, 
            {'error': 'Os usuários de destino e origem devem ser diferentes'})
