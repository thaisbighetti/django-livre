from uuid import uuid4
from django.db import models
from localflavor.br.models import BRCPFField
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name='Nome')
    cpf = BRCPFField('CPF ', blank=False, primary_key=True, unique=True)
    phone = PhoneNumberField(region='BR', blank=False, help_text='Formato DDD + Número',verbose_name='Telefone')
    email = models.EmailField(max_length=255, blank=False)
    creation = models.DateTimeField(auto_now=True)

    def __str__(self):
        details = f'Cliente: {self.name}, cpf: {self.cpf}'
        return details


class Account(models.Model):
    number = models.UUIDField(default=uuid4, verbose_name='Número da Conta')
    balance = models.PositiveIntegerField(default=5000, blank=True, verbose_name='Saldo')
    account_user = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='account_user_id', editable=False, primary_key=True, verbose_name='Cliente')

    def __str__(self):
        details = f'Conta: {self.number} | Saldo atual: {self.balance} '
        return details


class Transfer(models.Model):
    source_cpf = BRCPFField('CPF do usuário de origem', blank=False, unique=False)
    target_cpf = BRCPFField('CPF do usuário de destino', blank=False, unique=False, )
    value = models.FloatField(default=0, verbose_name='Valor',)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        details = f'De: {self.source_cpf} | Para: {self.target_cpf} | Valor: {self.value} | Data: {self.date}'
        return details


