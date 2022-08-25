from django.utils import timezone

from authapp.models import VerifyCode


def is_token_verify_expired(verify: VerifyCode) -> bool:
    now_date = timezone.now()
    if now_date >= verify.data_expired:
        return False
    return True


