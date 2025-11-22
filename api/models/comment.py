from django.db import models
from api.models.user import User
from api.models.post import Post



class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE , related_name="comments")
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    comment = models.TextField()
    
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s comment"