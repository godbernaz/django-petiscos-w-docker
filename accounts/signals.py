# accounts/signals.py
from allauth.account.signals import email_confirmation_sent, email_confirmed
from django.dispatch import receiver
from django.contrib import messages
from allauth.account.adapter import DefaultAccountAdapter

@receiver(email_confirmation_sent)
def custom_email_confirmation_sent(request, confirmation, **kwargs):
    # The 'confirmation' object contains the email information
    email = confirmation.email_address.email
    messages.info(
        request,
        f"Um pedido de verificação foi enviado para o email: {email}. Por favor, verifica a tua caixa de entrada."
    )

@receiver(email_confirmed)
def custom_email_confirmed(request, email_address, **kwargs):
    messages.success(
        request,
        f"O email {email_address.email} foi verificado com sucesso! Obrigado."
    )
    
class CustomAccountAdapter(DefaultAccountAdapter):
    def add_message(self, request, level, message_template, message_context=None, extra_tags=""):
        pass