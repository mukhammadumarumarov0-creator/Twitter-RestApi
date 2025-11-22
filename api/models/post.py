from django.db import models
from api.models.user import User
from django.core.validators import FileExtensionValidator


class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE , related_name="posts",null=True,blank=True)
    content = models.TextField()
    liked_user=models.ManyToManyField(User,related_name="liked_post",blank=True)
    viewed_user=models.ManyToManyField(User,related_name="viewed_post",blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s post "
    
class Media(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="mediafiles")
    media=models.FileField(upload_to="posts/media_files/",validators=[FileExtensionValidator(allowed_extensions=["jpeg","jpg","png","mp4"])])

