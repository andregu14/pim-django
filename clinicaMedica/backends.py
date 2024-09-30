from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import MedicoDentista, Recepcionista, Gestor

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = MedicoDentista.objects.get(email=username)
        except MedicoDentista.DoesNotExist:
            try:
                user = Recepcionista.objects.get(email=username)
            except Recepcionista.DoesNotExist:
                try:
                    user = Gestor.objects.get(email=username)
                except Gestor.DoesNotExist:
                    return None

        if user and check_password(password, user.senha):
            return user
        return None

    def get_user(self, user_id):
        try:
            return MedicoDentista.objects.get(pk=user_id)
        except MedicoDentista.DoesNotExist:
            try:
                return Recepcionista.objects.get(pk=user_id)
            except Recepcionista.DoesNotExist:
                try:
                    return Gestor.objects.get(pk=user_id)
                except Gestor.DoesNotExist:
                    return None
