from django.core.exceptions import ValidationError


class CustomValidationError(ValidationError):
    def __init__(self, message, code=None, params=None):
        self.code = code
        super().__init__(message, code=code, params=params)

    def to_dict(self):
        return {
            "code": self.code,
            "message": self.message,
        }
