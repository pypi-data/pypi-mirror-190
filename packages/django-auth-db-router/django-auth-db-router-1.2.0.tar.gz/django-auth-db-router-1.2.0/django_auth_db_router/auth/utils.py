import datetime

import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django_auth_db_router.auth.models import Token

User = get_user_model()

utc = pytz.timezone(settings.TIME_ZONE)


class ExpiringTokenAuthentication(TokenAuthentication):
    model = Token
    keyword = 'Bearer'

    def authenticate_credentials(self, key, request=None):
        models = self.get_model()

        try:
            token = models.objects.select_related("user").get(key=key)
        except models.DoesNotExist:
            raise AuthenticationFailed({"error": "Invalid or Inactive Token", "is_authenticated": False})

        if not token.user.is_active:
            raise AuthenticationFailed({"error": "Invalid user", "is_authenticated": False})

        if not token.authenticated:
            raise AuthenticationFailed({"error": "Inactive Token", "is_authenticated": False})

        now = datetime.datetime.now().replace(tzinfo=utc)

        if token.last_use < now - settings.TOKEN_TTL:
            token.deactivate()
            token.save()
            raise AuthenticationFailed({"error": "Token has expired", "token_status": False})

        token.last_use = now
        token.save()
        return token.user, token


def custom_create_token(token_model, user, serializer):
    token = token_model.objects.create(user=user)
    now = datetime.datetime.now()
    token.created = now
    token.save()
    return token

