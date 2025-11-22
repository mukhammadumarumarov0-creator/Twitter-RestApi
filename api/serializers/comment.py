from rest_framework import serializers
from api.models import Comment,User


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Comment
        fields=["comment","post"]


class MiniSeriazliser(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username","first_name","last_name"]

class CommentInDetailSerializer(serializers.ModelSerializer):
    user=MiniSeriazliser()
    class Meta:
        model=Comment
        fields="__all__"

  
