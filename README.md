# Django Livre bank

This is the final project of [Gama Academy](https://www.gama.academy/)'s  Construdelas Python training in partnership with [Juntos Somos +](https://www.juntossomosmais.com.br/).

The goal of this project was to develop an API using the Django Rest Framework.

## Running the project

This project uses [docker](https://www.docker.com/).
### Running the project

 docker build --tag app .
 
 docker run --publish 8000:8000 app

## Project routes

### USERS

- **GET** /create-user/ - Creates an user
- **POST** /create-user/ - Creates an user
- **GET** /user/<user_cpf> - Returns a specif user
- **PUT** /user/<user_cpf> - Returns a specif user
- **DELETE** /user/<user_cpf> - Returns a specif user
- **GET** /all-users/ - Lists all the users

### ACCOUNTS

- **GET** /all-accounts/ - Lists all the accounts
- **GET** /account/<user_cpf> - Returns a specif account

### TRANSFERS

- **GET** /transfer/ - Transfers amount from an account to another
- **POST** /transfer/ - Transfers amount from an account to another
- **GET** /all-tranfers/ - Lists all transfers
- **GET** /transfers-received/<user_cpf> - Lists all the transfers received by an user
- **GET** /transfers-performed/<user_cpf> - Lists all the transfers performed by an user

## Contributors
- [Amanda Luz](https://github.com/AmanddaLuz)
- [Giulia Coutinho](https://github.com/agiulsz)
- [Marília Ferreira](https://github.com/miachafer)
- [Teresa Antunes](https://github.com/teresantns)
- [Thais Bighetti](https://github.com/thaisbighetti)
 
 Watch out the API working [here](https://youtu.be/geU1rco1OHY).
