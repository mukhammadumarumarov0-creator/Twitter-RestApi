from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from rest_framework.response import Response
from rest_framework import status as st
import re


def send_code_to_email(email,code):
    text = f"Assalomu alaykum Twitter api uchun tastiqlash kodi : {code}"
    send_mail(
        subject="Confirmation Code",
        message=text,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )

def send_token_to_email(email,token):
    text = f"Assalomu alaykum Passwordni ozgartirish uchun token : {token}"
    send_mail(
        subject="Change Password Token",
        message=text,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )

def username_emial(user_input:str):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', user_input)


class MyResponse:
    def success(message,data=None):

        return Response(
            {
                "message" : message,
                "status" : True,
                "data": data

            } , status=st.HTTP_200_OK
        )
    
    def error(message,data=None):

        return Response(
            {
                "message" : message,
                "status" : False,
                "data": data

            } , status=st.HTTP_400_BAD_REQUEST
        )