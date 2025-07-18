from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthBackend(BaseBackend):
    def authenticate(self, request, email=None, REG_no=None, password=None, **kwargs):
        try:
            # Support login via email or REG_no
            if email:
                user = User.objects.filter(email=email).first()
            elif REG_no:
                user = User.objects.filter(REG_no=REG_no).first()
            else:
                return None

            # Check password
            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
