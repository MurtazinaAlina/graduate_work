# -*- coding: utf-8 -*-
import json

from braces.views import CsrfExemptMixin
from oauthlib.oauth2.rfc6749.endpoints.token import TokenEndpoint
from oauth2_provider.oauth2_backends import OAuthLibCore
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from oauth2_provider.models import Application, AccessToken
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import IN_QUERY, TYPE_INTEGER, Parameter as Param, TYPE_STRING, TYPE_FILE, IN_FORM, IN_BODY

from .oauth2_backends import KeepRequestCore
from .oauth2_endpoints import SocialTokenServer


class TokenView(CsrfExemptMixin, OAuthLibMixin, APIView):
    """
    Implements an endpoint to provide access tokens

    The endpoint is used in the following flows:

    * Authorization code
    * Password
    * Client credentials
    """
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = OAuthLibCore
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        # Use the rest framework `.data` to fake the post body of the django request.
        request._request.POST = request._request.POST.copy()
        for key, value in request.data.items():
            request._request.POST[key] = value

        url, headers, body, status = self.create_token_response(request._request)
        response = Response(data=json.loads(body), status=status)

        for k, v in headers.items():
            response[k] = v
        return response


# body для vk_auth
manual_parameters_vk_auth = [
    Param(name="grant_type", in_=IN_BODY, type=TYPE_STRING, required=True),
    Param(name="client_id", in_=IN_BODY, type=TYPE_STRING, required=True),
    Param(name="backend", in_=IN_BODY, type=TYPE_STRING, required=True),
    Param(name="token", in_=IN_BODY, type=TYPE_STRING, required=True)
]


@swagger_auto_schema(manual_parameters=manual_parameters_vk_auth)  # не сработало (((((((((((((((
class ConvertTokenView(CsrfExemptMixin, OAuthLibMixin, APIView):
    """
    Зарегистрировать пользователя через социальную сеть 'ВКонтакте'

    Возвращает access_token, который используется вместо email при прохождении аутентификации пользователя
    по пути 'user/login/'

    Пользователь будет сразу активен, подтверждение почты не требуется
    Рекомендуется после установить корректную почту и пароль через 'user/details/'

    В data необходимо передать следующие параметры:

    {
        "grant_type": "convert_token",
        "client_id": "Client id нашего application приложения DJANGO OAUTH TOOLKIT",
        "backend": "vk-oauth2",
        "token": "vk1.a._тут токен, выданный vk при авторизации приложения_"
    }

    __ТУТ НЕ УДАЛОСЬ РЕАЛИЗОВАТЬ ПАРАМЕТРИЗАЦИЮ ЗАПРОСА, ТЕСТИРОВАТЬ В POSTMAN__
    """
    # Implements an endpoint to convert a provider token to an access token
    # The endpoint is used in the following flows:
    # Authorization code
    # Client credentials

    # swagger_schema = None  # НЕ НАШЛА, КАК ДОБАВИТЬ ПАРАМЕТРИЗАЦИЮ В YASG =(, СЕРИАЛАЙЗЕР И РУЧНЫЕ ПАРАМЕТРЫ НЕ ВИДИТ =(

    server_class = SocialTokenServer
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = KeepRequestCore
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        # Use the rest framework `.data` to fake the post body of the django request.
        request._request.POST = request._request.POST.copy()
        for key, value in request.data.items():
            request._request.POST[key] = value

        url, headers, body, status = self.create_token_response(request._request)
        response = Response(data=json.loads(body), status=status)

        for k, v in headers.items():
            response[k] = v
        return response


class RevokeTokenView(CsrfExemptMixin, OAuthLibMixin, APIView):
    """
    Implements an endpoint to revoke access or refresh tokens
    """
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = OAuthLibCore
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        # Use the rest framework `.data` to fake the post body of the django request.
        request._request.POST = request._request.POST.copy()
        for key, value in request.data.items():
            request._request.POST[key] = value

        url, headers, body, status = self.create_revocation_response(request._request)
        response = Response(data=json.loads(body) if body else '', status=status if body else 204)

        for k, v in headers.items():
            response[k] = v
        return response


@api_view(['POST'])
@authentication_classes([OAuth2Authentication])
@permission_classes([permissions.IsAuthenticated])
def invalidate_sessions(request):
    client_id = request.POST.get("client_id", None)
    if client_id is None:
        return Response({
            "client_id": ["This field is required."]
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        app = Application.objects.get(client_id=client_id)
    except Application.DoesNotExist:
        return Response({
            "detail": "The application linked to the provided client_id could not be found."
        }, status=status.HTTP_400_BAD_REQUEST)

    tokens = AccessToken.objects.filter(user=request.user, application=app)
    tokens.delete()
    return Response({}, status=status.HTTP_204_NO_CONTENT)
