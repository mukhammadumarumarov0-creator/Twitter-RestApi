from django.urls import path
from .views import SendEmailCodeApiView,VerificationApiView,ResentCodeApiView,UpdateVerifedUserApiView

urlpatterns = [
   path("sign-up/",SendEmailCodeApiView.as_view()),
   path("verification/",VerificationApiView.as_view()),
   path("resend_code/",ResentCodeApiView.as_view()),
   path("update_user/",UpdateVerifedUserApiView.as_view())

  


]
