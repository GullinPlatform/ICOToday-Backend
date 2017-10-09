from django.utils import timezone

from ..rest_framework_jwt.settings import api_settings
from rest_framework.response import Response


def return_auth_token(account):
	# Get user auth token
	jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
	jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
	payload = jwt_payload_handler(account)
	token = jwt_encode_handler(payload)

	# Construct response object to set cookie
	response = Response()
	expiration = (timezone.now() +
	              api_settings.JWT_EXPIRATION_DELTA)
	response.set_cookie(api_settings.JWT_AUTH_COOKIE,
	                    token,
	                    expires=expiration,
	                    httponly=True)
	return response