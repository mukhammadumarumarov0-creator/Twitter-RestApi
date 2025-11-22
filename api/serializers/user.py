from rest_framework import serializers 
from api.models import User,DONE,ChangeUsersPassword
from api.utils import username_emial



class EmailSerializer(serializers.Serializer):
    email=serializers.EmailField()

    def validate_email(self,value):
        if User.objects.filter(email=value).filter(status=DONE).exists():
            raise serializers.ValidationError("User with such email already exists")
        return value


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
        if len(password) < 6:
            raise serializers.ValidationError("Password must be  at least 6 digits")
        return value


class LoginSerializer(serializers.Serializer):
    user_input = serializers.CharField(required=True)
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        user_input = attrs.get("user_input")

        # user_input email bo'lsa
        if username_emial(user_input):
            try:
                # Email orqali user topish
                user = User.objects.get(email=user_input, status=DONE)
                attrs["username"] = user.username  # ← username qaytariladi
                return attrs

            except User.DoesNotExist:
                raise serializers.ValidationError("Bunday emailli foydalanuvchi topilmadi")

        # user_input email emas — oddiy username sifatida qabul qilinadi
        attrs["username"] = user_input
        return attrs


class PasswordUpdateSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    reset_password = serializers.CharField(required=True, min_length=6)

    def validate_access_token(self, value):
        if not ChangeUsersPassword.objects.filter(access_token=value).last():
            raise serializers.ValidationError("Invalid or expired token")
        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["reset_password"]:
            raise serializers.ValidationError("Passwords don't match")
        return attrs




        



    

    
        

        
    
            



       
