import datetime

import pytz
from django.contrib.auth import login
from django.db import IntegrityError, transaction
from django.shortcuts import render
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from standard.response import ErrorCode, ErrorMessage, get_error_response

# Create your views here.
from .models import CustomUser
from .serializer import AccountSerializer, CustomAuthTokenSerializer


class SignupView(APIView):
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        signup_post_serializer = self.serializer_class(data=request.data)

        if not signup_post_serializer.is_valid():
            for field_name, field_errors in signup_post_serializer.errors.items():
                error_code = field_errors[0].code
                if error_code == "blank":
                    error_code = ErrorCode.INVALID_REQUEST
                    error_message = ErrorMessage.INVALID_REQUEST
                else:
                    error_message = str(field_errors[0])
                break
            return Response(
                get_error_response(
                    error_code=error_code,
                    error=error_message,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        username = signup_post_serializer.validated_data.get("username")
        email = signup_post_serializer.validated_data.get("email")
        password = signup_post_serializer.validated_data.get("password")
        full_name = signup_post_serializer.validated_data.get("full_name")
        age = signup_post_serializer.validated_data.get("age")
        gender = signup_post_serializer.validated_data.get("gender")

        try:
            with transaction.atomic():
                user_obj = CustomUser.objects.create(
                    username=username,
                    email=email,
                    full_name=full_name,
                    age=age,
                    gender=gender,
                    is_active=True,
                )
                user_obj.set_password(password)
                user_obj.save()

        except IntegrityError as e:
            return Response(
                get_error_response(
                    error_code=ErrorCode.INVALID_AGE,
                    error=ErrorMessage.INVALID_AGE,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = {
            "status": "success",
            "message": "User successfully registered!",
            "data": AccountSerializer(user_obj).data,
        }
        return Response(
            response,
            status=status.HTTP_201_CREATED,
        )


class JWTSignInView(APIView):
    """Handle login action."""

    serializer_class = CustomAuthTokenSerializer
    permission_classes = (AllowAny,)

    # @swagger_auto_schema(
    #     request_body=AuthTokenSerializer, responses={200: UserSerializer()}
    # )
    def post(self, request, format=None):
        serializer = self.serializer_class(
            context={"request": request}, data=request.data
        )

        if not serializer.is_valid():
            for field_name, field_errors in serializer.errors.items():
                error_code = field_errors[0].code
                if error_code == "blank":
                    error_code = ErrorCode.MISSING_FIELDS
                    error_message = ErrorMessage.MISSING_FIELDS
                else:
                    error_message = str(field_errors[0])
                break
            return Response(
                get_error_response(
                    error_code=error_code,
                    error=error_message,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.validated_data["user"]
        login(request, user)

        # Creating a JWT token
        refresh = TokenObtainPairSerializer.get_token(user)
        expiry = datetime.datetime.fromtimestamp(
            refresh.access_token.payload.get("exp"), tz=pytz.utc
        )

        # Calculate the current time in UTC timezone
        current_datetime = datetime.datetime.now(pytz.utc)

        remaining_seconds = (expiry - current_datetime).total_seconds()

        # Returning the token and the expiry
        data = {
            "access_token": str(refresh.access_token),
            "expiry_in": int(remaining_seconds),
        }

        response = {
            "status": "success",
            "message": "Access token generated successfully.",
            "data": data,
        }
        return Response(
            response,
            status=status.HTTP_200_OK,
        )
