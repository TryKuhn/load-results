import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.exceptions import ParseError

from api.controllers.yandexAuth import YandexAuth


def get_url(request):
    url = YandexAuth.get_code_yandex()
    return JsonResponse({'url': url})

@require_POST
def get_token(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data['code']

            token = YandexAuth.get_token_yandex(code=code)
            user_id = YandexAuth.add_user(token=token)

            return JsonResponse({'accessToken': token, 'userId': user_id})

        except KeyError as exc:
            raise ParseError(f"Ошибка! {exc}") from exc
    else:
        raise ParseError("This is not a POST request!")