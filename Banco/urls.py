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
     TransfersReceived,  AccountsView, MainPage, AccountView

from django.conf.urls import url
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

"""
Swagger is used in conjunction with a set of software tools
source software for designing, building, documenting, and using RESTful web services.
"""
schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainPage.as_view()),
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

"""
Routes to submit documentation:
- Requests;
- Returns
"""
# Swagger
urlpatterns += [
   url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
