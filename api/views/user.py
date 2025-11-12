from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import User
from api.serializers import EmailSerializer
from api.utils import send_code_to_email

class SendEmailCodeApiView(APIView):
    serializer_class=EmailSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email=serializer.validated_data.get("email")
        user=User.objects.create(email=email)

        send_code_to_email(email,user.get_verify_code())

        data = {
            "status" : True,
            "message" : "Verification code sent to your email address",
            "tokens" : user.get_token()
        }

        return Response(data)