from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils import timezone

NEW,CODE_VERIFIED,DONE = ("new" , "code_verifed" , "done")

class User(AbstractUser):
    status_choice = (
        (NEW,NEW),
        (CODE_VERIFIED,CODE_VERIFIED),
        (DONE,DONE)
    ) 

    phone_number=models.CharField(max_length=13 , null=True , blank=True)
    status=models.CharField(max_length=20,choices=status_choice,default=NEW)
    image=models.ImageField(upload_to="userprofle_photo/",validators=[FileExtensionValidator(allowed_extensions=["jpg","png","jpeg"])],null=True,blank=True)
    bio=models.TextField(null=True,blank=True)
    address=models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return self.username

class UserConfirmation(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="confirmations")
    code=models.PositiveIntegerField()
    is_expired=models.BooleanField(null=True,blank=True,default=False)
    expired_time=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def save(self,*args, **kwargs):
        self.expired_time=timezone.now()+timezone.timedelta(minutes=2)
        return super().save(*args, **kwargs)
    
    def isExpired(self):
        if self.expired_time > timezone.now():
            return False
        return True
    
    def __str__(self):
        return f"{self.user.username}'s confirmation code {self.code}"
    

