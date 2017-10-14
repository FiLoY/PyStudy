from django.contrib.auth import get_user_model
from .models import User


class AccountBackend(object):
    """Мой бекэнд для авторизации, используя почту или имя пользователя"""
    def authenticate(self, username=None, password=None, **kwargs):
        user_model = get_user_model()
        try:
            # authenticate with email address
            user = user_model.objects.get(email__iexact=username)
        except user_model.DoesNotExist:
            try:
                # authenticate with username
                user = user_model.objects.get(username__iexact=username)
            except user_model.DoesNotExist:
                return None
            else:
                if getattr(user, 'is_active', False) and user.check_password(password):
                    return user
        else:
            if getattr(user, 'is_active', False) and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
