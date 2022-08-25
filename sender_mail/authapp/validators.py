from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class AgeMinValueValidator(MinValueValidator):
    message = _('Your age is not allowed to register, only from the age of 18')
