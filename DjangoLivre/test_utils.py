"""
Utilities that are being used in our tests in tests.py. We have a function to 
generate random valid cpfs, to post valid clients, and a function that posts clients
"""
from datetime import datetime
from rest_framework.test import RequestsClient

def generate_valid_cpf():  
    """
    This function generates a random valid CPF. We are going to use it for populating the
    tables and testing our API. (return cpf in string format)
    """
    from random import randint
    numero = str(randint(100000000, 999999999))
    novo_cpf = numero  # variável que vamos criar para conferir o cpf (tirando os dois últimos digitos)
    cpf_lista = [int(i) for i in novo_cpf]

    maxs = 10
    while True:
        soma = 0
        for n, r in enumerate(range(maxs, 1, -1)):
            soma += r * cpf_lista[n]

        d = 0 if (11 - (soma % 11)) > 9 else (11 - (soma % 11))

        novo_cpf += str(d)  # colocando o digito novo no cpf
        cpf_lista.append(d)  # colocando o digito na lista do cpf
        if len(novo_cpf) < 11:
            maxs += 1  # aumentando o range do for para 11
            continue
        return novo_cpf

def post_two_clients():
    """
    Note: this function was added after test_should_post_users_and_create_accounts, so we
    are already sure the 'create-user/' endpoint is working properly.

    Now we are sure our post method for clients works, we are going to use this function
    to post clients (and consequently create accounts) to test the remaining endpoints
    and functionalities of our API (transfers and account-client relation).
    """

    client_data = {'cpf': generate_valid_cpf(), 
    'name': 'name_3', 
    'phone': '+5531987654321', 
    'email': 'name_3@gmail.com',
    'date': datetime.now() 
    }
    client_data_2 = {'cpf': generate_valid_cpf(), 
    'name': 'name_4', 
    'phone': '+5541987654321', 
    'email': 'name_4@gmail.com',
    'date': datetime.now() 
    }

    client = RequestsClient()
    client.post('http://127.0.0.1:8000/create-user/', client_data)
    client.post('http://127.0.0.1:8000/create-user/', client_data_2)
