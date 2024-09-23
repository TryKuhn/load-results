from os import environ

from requests import get, post
from requests.models import PreparedRequest

from api.models.user import User


class YandexAuth:
    TIMEOUT = 30

    client_id = environ.get('YANDEX_CLIENT_ID')
    client_secret = environ.get('YANDEX_CLIENT_SECRET')
    redirect_uri = environ.get('YANDEX_REDIRECT_URI')

    prepared_request = PreparedRequest()

    @staticmethod
    def get_code_yandex(host: str = 'https://oauth.yandex.ru/authorize'):
        params = {'response_type': 'code', 'client_id': f'{YandexAuth.client_id}',
                  'client_secret': f'{YandexAuth.client_secret}',
                  'redirect_uri': f'{YandexAuth.redirect_uri}'}

        YandexAuth.prepared_request.prepare_url(host, params)
        request_code = get(f'{YandexAuth.prepared_request.url}',
                                    timeout=YandexAuth.TIMEOUT)
        if request_code.status_code != 200:
            raise RuntimeError(f'Yandex API error: status code -> {request_code.status_code}')

        return request_code.url

    @staticmethod
    def get_token_yandex(host: str = 'https://oauth.yandex.ru/token', code: str = ''):
        params = {'grant_type': 'authorization_code', 'code': code, 'client_id': f'{YandexAuth.client_id}',
                  'client_secret': f'{YandexAuth.client_secret}'}

        oauth_token = post(url=host, data=params,
                                    timeout=YandexAuth.TIMEOUT)
        if oauth_token.status_code != 200:
            raise RuntimeError(f'Yandex API error: status code -> {oauth_token.status_code}')
        access_token = oauth_token.json()['access_token']

        return access_token

    @staticmethod
    def info_user_yandex(token: str, host: str = 'https://oauth.yandex.ru/info'):
        params = {'oauth_token': token, 'format': 'json'}

        YandexAuth.prepared_request.prepare_url(host, params)
        info = get(f'{YandexAuth.prepared_request.url}',
                            timeout=YandexAuth.TIMEOUT)
        if info.status_code != 200:
            raise RuntimeError(f'Yandex API error: status code -> {info.status_code}')

        return info.json()

    @staticmethod
    def add_user(token):
        info = YandexAuth.info_user_yandex(token)

        user_yandex_id = info['id']
        user_username = info['login']
        user_first_name = info['first_name']
        user_last_name = info['last_name']
        user_email = info['default_email']
        user_token = token

        user = {
            'yandex_id': user_yandex_id,
            'username': user_username,
            'first_name': user_first_name,
            'last_name': user_last_name,
            'email': user_email,
            'token': user_token
        }

        User.objects.update_or_create(yandex_id=user_yandex_id, defaults=user)

        return User.objects.get(yandex_id=user_yandex_id).id