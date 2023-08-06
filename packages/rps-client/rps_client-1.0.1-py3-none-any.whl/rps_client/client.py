import http.client
import json
from rps_client.config import BASE_URL, RPS_PATH, RPS_API_KEY, RPS_SERVICE_PATH
from rps_client.models import RpsHookRequest, RpsHookResponse


def make_request(path, data, url=BASE_URL, method='POST', headers={'content-type': 'application/json'}):
    if method is None:
        method = 'POST'

    if url is None:
        url = BASE_URL

    if url.startswith('http://'):
        url = url.replace('http://', '')
        connection = http.client.HTTPConnection(url)
    else:
        url = url.replace('https://', '')
        connection = http.client.HTTPSConnection(url)

    # Append headers to request
    if headers is None:
        headers = {'content-type': 'application/json'}

    if data is not None:
        if isinstance(data, str):
            json_data = data
        else:
            json_data = json.dumps(data)

    connection.request(method, path, json_data, headers)
    response = connection.getresponse()
    return response.read().decode()


def rps_request(request: RpsHookRequest, api_key: str | None = None, base_url: str | None = None, path: str | None = RPS_PATH) -> RpsHookResponse:
    headers = {
        'content-type': 'application/json',
        'Authorization': 'api-key ' + api_key,
    }

    if base_url is None:
        base_url = BASE_URL

    if api_key is None:
        api_key = RPS_API_KEY

    if path is None:
        path = RPS_PATH

    response_str = make_request(
        url=base_url,
        path=path,
        data=request.to_json(),
        headers=headers,
        method='POST',
    )

    return RpsHookResponse.from_json(response_str)


def rps_webhook(request: RpsHookRequest, api_key: str | None = None, base_url: str | None = None) -> RpsHookResponse:
    return rps_request(request, api_key, base_url, path=RPS_PATH)


def rps_service(request: RpsHookRequest, api_key: str | None = None, base_url: str | None = None) -> RpsHookResponse:
    return rps_request(request, api_key, base_url, path=RPS_SERVICE_PATH)
