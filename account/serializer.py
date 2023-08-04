import re

from django.contrib.auth import authenticate
from rest_framework import serializers

from standard.response import ErrorCode, ErrorMessage

from .models import CustomUser
from .validators import CustomValidationError

# class AccountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ("email", "username", "password", "full_name", "age", "gender")

#         extra_kwargs = {
#             "email": {"required": True},
#             "username": {"required": True},
#             "full_name": {"required": True},
#             "age": {"required": True},
#             "gender": {"required": True},
#             "password": {
#                 "write_only": True,
#                 "required": True,
#                 "validators": [PasswordValidator()],
#             },
#         }


class AccountSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    full_name = serializers.CharField(required=True)
    age = serializers.IntegerField(required=False)
    gender = serializers.CharField(required=True)

    def validate(self, data):
        # Custom validation across multiple fields can be done here
        if any(value is None for value in data.values()):
            error_message = ErrorCode.INVALID_REQUEST
            error_code = ErrorMessage.INVALID_REQUEST
            raise CustomValidationError(message=error_message, code=error_code)
        return data

    def validate_email(self, value):
        user_obj = None
        try:
            user_obj = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            pass
        if user_obj:
            error_message = ErrorCode.EMAIL_EXISTS
            error_code = ErrorMessage.EMAIL_EXISTS
            raise CustomValidationError(message=error_message, code=error_code)
        return value

    def validate_username(self, value):
        user_obj = None
        try:
            user_obj = CustomUser.objects.get(username=value)
        except CustomUser.DoesNotExist:
            pass
        if user_obj:
            error_message = ErrorCode.USERNAME_EXISTS
            error_code = ErrorMessage.USERNAME_EXISTS
            raise CustomValidationError(message=error_message, code=error_code)
        return value

    def validate_password(self, value):
        if (
            len(value) < 8
            or not any(char.isupper() for char in value)
            or not any(char.islower() for char in value)
            or not any(char.isdigit() for char in value)
            or not re.search(r'[!@#$%^&*(),.?":{}|<>]', value)
        ):
            error_message = ErrorCode.INVALID_PASSWORD
            error_code = ErrorMessage.INVALID_PASSWORD
            raise CustomValidationError(message=error_message, code=error_code)
        return value

    def validate_age(self, value):
        if value <= 0:
            error_message = ErrorCode.INVALID_AGE
            error_code = ErrorMessage.INVALID_AGE
            raise CustomValidationError(message=error_message, code=error_code)
        return value

    def validate_gender(self, value):
        if value not in ["male", "female", "non-binary"]:
            error_message = ErrorCode.GENDER_REQUIRED
            error_code = ErrorMessage.GENDER_REQUIRED
            raise CustomValidationError(message=error_message, code=error_code)
        return value


class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(
        required=True, trim_whitespace=False, write_only=True
    )
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            if not user:
                error_message = ErrorCode.INVALID_CREDENTIALS
                error_code = ErrorMessage.INVALID_CREDENTIALS
                raise CustomValidationError(message=error_message, code=error_code)
        else:
            error_message = ErrorCode.MISSING_FIELDS
            error_code = ErrorMessage.MISSING_FIELDS
            raise CustomValidationError(message=error_message, code=error_code)

        attrs["user"] = user
        return attrs
