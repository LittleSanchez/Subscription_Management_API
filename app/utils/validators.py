import re


class PasswordValidationError(Exception):
    pass


def validate_password(password: str) -> None:
    if len(password) < 8:
        raise PasswordValidationError("Password must be at least 8 characters long")
    if not any(c.isalpha() for c in password):
        raise PasswordValidationError("Password must contain at least one letter")
    if not any(c.isdigit() for c in password):
        raise PasswordValidationError("Password must contain at least one number")
