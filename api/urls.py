from django.urls import path
from .views import SendEmailCodeApiView

urlpatterns = [
   path("sign-up/",SendEmailCodeApiView.as_view())
]
