from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from . import settings

def get_email_host(saloon):
    connection = get_connection(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_PORT, 
        username=saloon.admin.host_email, 
        password=saloon.admin.host_passcode, 
        use_tls=settings.EMAIL_USE_TLS,)
    return connection