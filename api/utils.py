from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from rest_framework.response import Response
from rest_framework import status as st


def send_code_to_email(email,code):
    text = f"Assalomu alaykum Twitter api uchun tastiqlash kodi : {code}"
    send_mail(
        subject="Confirmation Code",
        message=text,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )



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