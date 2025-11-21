from django.urls import path
from .views import SendEmailCodeApiView,VerificationApiView,ResentCodeApiView,UpdateVerifedUserApiView,LoginUserApiView,\
   GetChangePasswordToken,PasswordUpdateView

urlpatterns = [
   path("sign-up/",SendEmailCodeApiView.as_view()),
   path("verification/",VerificationApiView.as_view()),
   path("resend_code/",ResentCodeApiView.as_view()),
   path("update_user/",UpdateVerifedUserApiView.as_view()),
   path("login_user/",LoginUserApiView.as_view()),
   path("password_token/",GetChangePasswordToken.as_view()),
   path("change_password/",PasswordUpdateView.as_view()),




  


]
