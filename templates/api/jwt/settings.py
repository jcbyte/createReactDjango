REST_FRAMEWORK = {
  "DEFAULT_AUTHENTICATION_CLASSES": [
      "rest_framework_simplejwt.authentication.JWTAuthentication",
  ],
}

from datetime import timedelta

SIMPLE_JWT = {
  "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
  "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

AUTH_USER_MODEL = "api.User"
