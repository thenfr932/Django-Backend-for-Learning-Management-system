from rest_framework import serializers
from django.contrib.auth import authenticate , get_user_model


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(
            email=data["email"],
            password=data["password"]
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user


class RegisterSerializer(serializers.ModelSerializer): 
    password = serializers.CharField(write_only=True)
    class Meta:
        model = get_user_model()
        fields = ["email","username","password"]

    def create(self, data):
        newuser=get_user_model().objects.create_user(**data)
        return newuser