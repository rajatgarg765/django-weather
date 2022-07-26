from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from account.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=User
        fields=['username','name','password','password2']
        extra_kwargs={
           'password': {'write_only':True}
        }
    #validate passowrd and confirm password while registration
    def validate(self,attrs):
        password=attrs.get("password")
        password2=attrs.get("password2")
        if password!=password2:
            raise serializers.ValidationError('Passwords Do not match')
        return attrs

    def create(self,validate_data):
        return User.objects.create_user(**validate_data)
    

class UserLoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField(max_length=255)
    class Meta:
        model=User
        fields=['username','password']

