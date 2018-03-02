from django.core.exceptions import ValidationError


def range_validator(value):
    if value not in range(2000, 2004 + 1):
        raise ValidationError("{} rok z poza przedziau 2000-2004!".format(value))
