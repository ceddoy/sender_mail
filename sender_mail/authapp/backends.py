from django.contrib.auth.backends import ModelBackend, UserModel


class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

    # def user_can_authenticate(self, user):
    #     is_verify = getattr(user, 'is_verify')
    #     if not is_verify:
    #         return is_verify
    #     return getattr(user, 'is_active')
