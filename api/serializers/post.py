from rest_framework import serializers
from api.models import Post,User


class CreatePostSerialzer(serializers.Serializer):
       content=serializers.CharField(required=True)

class DeletePostSerialzer(serializers.Serializer):
       pk=serializers.CharField(required=True)

       def validate_pk(self,value):
            if not Post.objects.filter(pk=value).exists():
                  raise serializers.ValidationError("No such post")
            return value

class UserMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

class MyPostsSerialzer(serializers.ModelSerializer):
    user = UserMiniSerializer()

    class Meta:
        model = Post
        fields = "__all__"

class PostsLikeSeriazlier(serializers.ModelSerializer):
     user=UserMiniSerializer()
     class Meta:
          model=Post
          fields = "__all__"      
       
                  

    


        