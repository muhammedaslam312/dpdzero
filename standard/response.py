class ErrorCode:
    INVALID_REQUEST = "INVALID_REQUEST"
    USERNAME_EXISTS = "USERNAME_EXISTS"
    EMAIL_EXISTS = "EMAIL_EXISTS"
    INVALID_PASSWORD = "INVALID_PASSWORD"
    INVALID_AGE = "INVALID_AGE"
    GENDER_REQUIRED = "GENDER_REQUIRED"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    MISSING_FIELDS = "MISSING_FIELDS"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    KEY_NOT_FOUND = "KEY_NOT_FOUND"
    INVALID_TOKEN = "INVALID_TOKEN"
    INVALID_KEY = "INVALID_KEY"
    INVALID_VALUE = "INVALID_VALUE"


class ErrorMessage:
    INVALID_REQUEST = "Invalid request. Please provide all required fields: username, email, password, full_name."
    USERNAME_EXISTS = (
        "The provided username is already taken. Please choose a different username."
    )
    EMAIL_EXISTS = "The provided email is already registered. Please use a different email address."
    INVALID_PASSWORD = "The provided password does not meet the requirements. Password must be at least 8 characters long and contain a mix of uppercase and lowercase letters, numbers, and special characters."
    INVALID_AGE = "Invalid age value. Age must be a positive integer."
    GENDER_REQUIRED = "Gender field is required. Please specify the gender (e.g., male, female, non-binary)."
    INTERNAL_SERVER_ERROR = "An internal server error occurred. Please try again later."
    INVALID_CREDENTIALS = (
        "Invalid credentials. The provided username or password is incorrect."
    )
    MISSING_FIELDS = "Missing fields. Please provide both username and password."
    INTERNAL_ERROR = "Internal server error occurred. Please try again later."
    KEY_NOT_FOUND = "The provided key does not exist in the database."
    INVALID_TOKEN = "Invalid access token provided"
    INVALID_KEY = "The provided key is not valid or missing."
    INVALID_VALUE = "The provided value is not valid or missing."


# customize error response
def get_error_response(error_code: str, error: str):
    return {"status": "error", "code": error_code, "message": error}
