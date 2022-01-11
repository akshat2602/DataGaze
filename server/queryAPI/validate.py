from django.core.exceptions import ValidationError


def validate_field(validating_var, CHOICES):
    if validating_var not in CHOICES:
        raise ValidationError("invalid type of filter")