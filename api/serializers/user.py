from rest_framework import serializers 
from api.models import User

class EmailSerializer(serializers.Serializer):
    email=serializers.EmailField()


class CodeVirificationSerializer(serializers.Serializer):
    code=serializers.CharField(required=True)

    def validate_code(self,value):
        if len(value) < 4:
            raise serializers.ValidationError("Code must be 4 digits")
        return value


class UpdateValidatedUserSerializer(serializers.Serializer):
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)
    reset_password=serializers.CharField(required=True)



    def validate_first_name(self,value):
        if not value.isalpha():
            raise serializers.ValidationError("First name can't contain any numbers or symbols")
        return value
    
    def validate_last_name(self,value):
        if not value.isalpha():
            raise serializers.ValidationError("Last name can't contain any numbers or symbols")
        return value
    
    def validate_username(self,value):
        if User.objects.filter(username=value):
            raise serializers.ValidationError("This username already exists please enter other one")
        return value
    
    def validate(self,value):
        password=value['password']
        password2=value['reset_password']

        if password != password2:
            raise serializers.ValidationError("Possword and reset password don't match")
        if len(password) < 4:
            raise serializers.ValidationError("Password must be  at least 4 digits")
        return value

   
      