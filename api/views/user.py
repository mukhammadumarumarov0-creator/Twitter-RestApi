from rest_framework.views import APIView
from api.models import User,CODE_VERIFIED,DONE,ChangeUsersPassword
from api.serializers import EmailSerializer,CodeVirificationSerializer,UpdateValidatedUserSerializer,LoginSerializer,\
   PasswordUpdateSerializer
from api.utils import send_code_to_email,send_token_to_email,MyResponse
from rest_framework.permissions import IsAuthenticated,AllowAny
from django.contrib.auth import authenticate
from api.permission import IsAuthAndDone


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

        
class LoginUserApiView(APIView):
    serializer_class = LoginSerializer

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        password=serializer.validated_data.get("password")
        username=serializer.validated_data.get("username")

        user=authenticate(request,username=username,password=password)
        if user is not None:
            return MyResponse.success(
                message=" User Logged in seccessfuly",
                data=user.get_token()
            )

        return MyResponse.error(
            "username or password or email is not valid"
        )



class GetChangePasswordToken(APIView):
    permission_classes = [IsAuthAndDone]
    def get(self, request):
        try:
            user = User.objects.get(username=request.user.username)
            users_token = ChangeUsersPassword.objects.filter(user=user).last()
        except :
            return MyResponse.error("No such user")

        if not users_token:
            users_token = ChangeUsersPassword.objects.create(user=user)
        if not users_token.is_active:
            send_token_to_email(
                email=user.email,
                token=users_token.access_token
            )
            users_token.active_mode()

            return MyResponse.success(
                "Token has been sent to your email",
                users_token.access_token
            )
        
        return MyResponse.error(
            "Token already has been sent to your email"
        )
    


class PasswordUpdateView(APIView):
    serializer_class = PasswordUpdateSerializer
    permission_classes = [AllowAny]

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
       
        try:
            user_p=ChangeUsersPassword.objects.get(access_token=serializer.validated_data.get("access_token"))
            user=User.objects.get(username=user_p.user.username)
            user.set_password(serializer.validated_data.get("new_password"))
            user_p.is_active=False
            user.save()
            user_p.save()
        except:
            return MyResponse.error("Invalid data was entered")

        return MyResponse.success("Password has been updated successfully")



        


       
        

    
   





            
            



