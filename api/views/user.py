from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import User,UserConfirmation,CODE_VERIFIED,DONE
from api.serializers import EmailSerializer,CodeVirificationSerializer,UpdateValidatedUserSerializer
from api.utils import send_code_to_email,MyResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import UpdateAPIView

class SendEmailCodeApiView(APIView):
    serializer_class=EmailSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email=serializer.validated_data.get("email")
        user=User.objects.create(email=email)

        send_code_to_email(email,user.get_verify_code())
        return MyResponse.success(message="Verification code sent to your email address",data=user.get_token())
   

class VerificationApiView(APIView):
    permission_classes=[IsAuthenticated]
    serializer_class=CodeVirificationSerializer
    def post(self,request):
        user=request.user
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code=serializer.validated_data.get("code")
        if self.code_verification(code,user):

             return MyResponse.success(
                message = "User's code verified",
                data = user.get_token()
            )
        return MyResponse.success(
             message = "code dosen't match or expired",
            )

    
    def code_verification(self,code:str,user:User):
        validate_code=user.confirmations.order_by("-created_at").first()
        if validate_code.code == code and not validate_code.is_expired():
            user.status = CODE_VERIFIED
            user.save()
            return True


class ResentCodeApiView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        user=request.user
        if not user.confirmations.order_by("-created_at").first().is_expired():
            return MyResponse.error(message="Code hasn't been expired yet")
        return MyResponse.success(message="Verification code sent to your email address",data=user.get_token())
       
 
class UpdateVerifedUserApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateValidatedUserSerializer
    
    def put(self,request):
        serializer=self.serializer_class(data=request.data)
        user=request.user
        if user.status == CODE_VERIFIED or user.status == DONE:
            user.username = ""
            user.save()
            
            serializer.is_valid(raise_exception=True)
            valid_user=User.objects.get(id=user.id)
            s=serializer.validated_data 

            valid_user.first_name=s.get('first_name')
            valid_user.last_name=s.get('last_name')
            valid_user.username=s.get('username')
            valid_user.set_password(s.get('password'))
            valid_user.status=DONE
            valid_user.save()

            data = {
                "first name" : valid_user.first_name,
                "last name" : valid_user.last_name,
                "username" : valid_user.username,
                "status": valid_user.status,
                "password" : valid_user.password,
            }

            return MyResponse.success(
                message="User updated seccessfuly",
                data=data
            )
        return MyResponse.error(
                message="You should pass through verifaction first"
            )

        

    


    
   





            
            



