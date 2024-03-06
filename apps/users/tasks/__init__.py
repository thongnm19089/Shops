from rest_framework.response import Response
from django.core.mail import send_mail, EmailMessage
from rest_framework import status
from django.conf import settings
from django.contrib.auth import get_user_model
import random

from celery import shared_task
from config import celery_app

@celery_app.task()
def my_mail():
    email = "ilovelonelybaby@gmail.com"
    # user = get_user_model().objects.get(email=email)
    # user.code = code()
    # user.save()
    subject = "AttapHouse"
    msg     = "Your code is (use one-time): " + code()
    to      = str(email)
    res     = send_mail(subject, msg, settings.EMAIL_HOST_USER, [to])
    if(res == 1):
        msg = "Mail Sent Successfully."
    else:
        msg = "Mail Sending Failed."
    
    # return Response(msg, status=status.HTTP_200_OK)

def code(n=6,flag=1):
    code = ''
    for i in range(n):
        num = str(random.randint(0,9))
        if flag:
            lower = chr(random.randint(65,90))
            upper = chr(random.randint(97,122))
            num = random.choice([num,lower,upper])
        code += num
    return code

def send_email_review(emails, msg):
        subject = 'REVIEW PROFESSIONAL'
        msg = EmailMessage(subject, msg, settings.EMAIL_HOST_USER, emails)
        msg.content_subtype = "html"
        msg.send()
        
