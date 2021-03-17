from django.core.validators import RegexValidator


zipcode_validator = RegexValidator(
    "^[0-9]{5}(?:-[0-9]{4})?$",
    "Either provide a 5 or 9 digit zipcode Ex: 12345 or 12345-1234",
)
