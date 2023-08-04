from drf_yasg.utils import no_body, swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.validators import CustomValidationError
from standard.response import ErrorCode, ErrorMessage, get_error_response

from .models import DataModel

# Create your views here.


class DataMultiView(APIView):
    permission_classes = [IsAuthenticated]

    class DataPostSerializer(serializers.Serializer):
        key = serializers.CharField(required=True)
        value = serializers.CharField(required=True)

    # @swagger_auto_schema(
    #     request_body=DataPostSerializer,
    #     responses={"status": "success", "message": "Data stored successfully."},
    # )
    def post(self, *args, **kwargs):
        data_post_serializer = self.DataPostSerializer(data=self.request.data)

        if not data_post_serializer.is_valid():
            for field_name, field_errors in data_post_serializer.errors.items():
                code = field_errors[0].code
                if code == "blank" and field_name == "key":
                    error_code = ErrorCode.INVALID_KEY
                    error_message = ErrorMessage.INVALID_KEY
                else:
                    error_code = ErrorCode.INVALID_VALUE
                    error_message = ErrorMessage.INVALID_VALUE
                break
            return Response(
                get_error_response(
                    error_code=error_code,
                    error=error_message,
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        key = data_post_serializer.validated_data.get("key")
        value = data_post_serializer.validated_data.get("value")

        DataModel.objects.create(
            key=key,
            value=value,
        )

        response = {"status": "success", "message": "Data stored successfully"}
        return Response(
            response,
            status=status.HTTP_201_CREATED,
        )


class DataView(APIView):
    permission_classes = [IsAuthenticated]

    class KwargsValidationSerializer(serializers.Serializer):
        key = serializers.CharField(required=True)

    class PatchDataSerializer(serializers.Serializer):
        value = serializers.CharField(required=False)

    class DataModelSerializer(serializers.ModelSerializer):
        class Meta:
            model = DataModel
            fields = ("key", "value")

    # @swagger_auto_schema(
    #     request_body=no_body,
    #     responses={"status": "success", "data": DataModelSerializer},
    # )
    def get(self, *args, **kwargs):
        kwargs_serializer = self.KwargsValidationSerializer(data=kwargs)

        if not kwargs_serializer.is_valid():
            return Response(
                kwargs_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        key = kwargs_serializer.validated_data.get("key")
        try:
            data_obj = DataModel.objects.get(key=key)

        except DataModel.DoesNotExist:
            return Response(
                get_error_response(
                    error_code=ErrorCode.KEY_NOT_FOUND, error=ErrorMessage.KEY_NOT_FOUND
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = {
            "status": "success",
            "data": self.DataModelSerializer(data_obj).data,
        }
        return Response(response, status=status.HTTP_200_OK)

    def patch(self, *args, **kwargs):
        kwargs_serializer = self.KwargsValidationSerializer(data=kwargs)

        if not kwargs_serializer.is_valid():
            return Response(
                kwargs_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        key = kwargs_serializer.validated_data.get("key")
        try:
            data_obj = DataModel.objects.get(key=key)

        except DataModel.DoesNotExist:
            return Response(
                get_error_response(
                    error_code=ErrorCode.KEY_NOT_FOUND, error=ErrorMessage.KEY_NOT_FOUND
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )

        data_patch_serializer = self.PatchDataSerializer(self.request.data)

        if not data_patch_serializer.is_valid():
            return Response(
                data_patch_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        value = data_patch_serializer.validated_data.get("value", None)
        if value:
            data_obj.value = value
        data_obj.save()

        response = {"status": "success", "message": "Data updated successfully"}
        return Response(response, status=status.HTTP_200_OK)

    def delete(self, *args, **kwargs):
        kwargs_serializer = self.KwargsValidationSerializer(data=kwargs)

        if not kwargs_serializer.is_valid():
            return Response(
                kwargs_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        key = kwargs_serializer.validated_data.get("key")
        try:
            data_obj = DataModel.objects.get(key=key)

        except DataModel.DoesNotExist:
            return Response(
                get_error_response(
                    error_code=ErrorCode.KEY_NOT_FOUND, error=ErrorMessage.KEY_NOT_FOUND
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        data_obj.delete()

        response = {"status": "success", "message": "Data deleted successfully."}
        return Response(response, status=status.HTTP_200_OK)
