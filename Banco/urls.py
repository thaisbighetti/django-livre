"""Banco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from DjangoLivre.views import CreateUser, UserView, CreateTransfer, TransfersView, UserSearch, TransfersPerformed,\
     TransfersReceived,  AccountsView, MainPage, AccountView, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('n/', MainPage.as_view()),
    path('create-user/', CreateUser.as_view()),
    path('user/<str:cpf>/', UserSearch.as_view()),
    path('all-users/', UserView.as_view()),
    path('transfer/', CreateTransfer.as_view()),
    path('all-transfers/', TransfersView.as_view()),
    path('transfers-received/<str:cpf>/', TransfersReceived.as_view()),
    path('transfers-performed/<str:cpf>/', TransfersPerformed.as_view()),
    path('all-accounts/', AccountsView.as_view()),
    path('account/<str:cpf>/', AccountView.as_view()),


]