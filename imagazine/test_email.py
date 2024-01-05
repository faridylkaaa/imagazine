from django.core.mail import send_mail

send_mail(
    'Test Subject',
    'Test message body',
    'faridylkaaa@yandex.ru',
    ['FaridBoss777@mail.ru'],
    fail_silently=False,
)