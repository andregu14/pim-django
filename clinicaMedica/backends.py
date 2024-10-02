from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from .models import MedicoDentista, Recepcionista, Gestor

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        for model in [MedicoDentista, Recepcionista, Gestor]:
            try:
                user = model.objects.get(email=username)
                if user and check_password(password, user.password):
                    self._update_last_login(user)
                    return user
            except model.DoesNotExist:
                continue
        return None

    def get_user(self, user_id):
        for model in [MedicoDentista, Recepcionista, Gestor]:
            try:
                return model.objects.get(pk=user_id)
            except model.DoesNotExist:
                continue
        return None

    def _update_last_login(self, user):
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])