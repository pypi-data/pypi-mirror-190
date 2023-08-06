import json
import uuid

from rps_client.utils import current_milli_time, safe_get_value_from_dict


class RpsClientOptions:
    def __init__(self,
                 base_url: str | None = None,
                 api_key: str | None = None,
                 ):
        self.base_url = base_url
        self.api_key = api_key

    def __repr__(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def __str__(self):
        return self.__repr__()

    # Create Builder
    @staticmethod
    def builder():
        return RpsClientOptionsBuilder()


class RpsClientOptionsBuilder:
    def __init__(self):
        self._base_url: str | None = None
        self._api_key: str | None = None

    def base_url(self, base_url: str):
        self._base_url = base_url
        return self

    def api_key(self, api_key: str):
        self._api_key = api_key
        return self

    def build(self) -> RpsClientOptions:
        return RpsClientOptions(
            base_url=self._base_url,
            api_key=self._api_key,
        )


class RpsHookRequest:
    def __init__(self, type: str | None, data=None, details: dict = None,):
        self.id = str(uuid.uuid4())
        self.data = data
        self.type = type
        self.details = details
        self.createdAt = current_milli_time()
        self.sendAt = None

    def add_details(self, key, value):
        if self.details is None:
            self.details = {}

        self.details[key] = value

    def add_send_at(self, send_at: int):
        self.sendAt = send_at

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def from_json(json_string):
        data = json.loads(json_string)
        return RpsHookRequest(
            type=safe_get_value_from_dict(data, 'type'),
            data=safe_get_value_from_dict(data, 'data'),
            details=safe_get_value_from_dict(data, 'details'),
        )

    def __repr__(self):
        return self.to_json()


class RpsHookResponse:
    def __init__(self, status: int, message: str | None, data=None, error: str | None = None):
        self.status = status
        self.data = data
        self.message = message
        self.error = error

    def is_error(self):
        return self.error != None and (self.status != 200 and self.status != 201)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @staticmethod
    def from_json(json_string):
        data = json.loads(json_string)
        return RpsHookResponse(
            status=safe_get_value_from_dict(data, 'status'),
            message=safe_get_value_from_dict(data, 'message'),
            data=safe_get_value_from_dict(data, 'data'),
            error=safe_get_value_from_dict(data, 'error'),
        )

    def __repr__(self):
        return self.to_json()


class RpsIssuer:
    def __init__(self, code: str, name: str, username: str):
        self.name = name
        self.code = code
        self.username = username

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @ staticmethod
    def from_json(json_string):
        data = json.loads(json_string)
        return RpsIssuer(
            code=safe_get_value_from_dict(data, 'code'),
            name=safe_get_value_from_dict(data, 'name'),
            username=safe_get_value_from_dict(data, 'username'),
        )

    @staticmethod
    def from_dict(data):
        return RpsIssuer(
            code=safe_get_value_from_dict(data, 'code'),
            name=safe_get_value_from_dict(data, 'name'),
            username=safe_get_value_from_dict(data, 'username'),
        )

    def __repr__(self):
        return self.to_json()


class RpsResponse:
    def __init__(self, id: str, type: str, data=None, issuer: RpsIssuer = None, createdAt: int = None):
        self.id = id
        self.type = type
        self.data = data
        self.issuer = issuer
        self.createdAt = createdAt

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    @ staticmethod
    def from_json(json_string):
        data = json.loads(json_string)
        resp_data = safe_get_value_from_dict(data, 'data')
        id = safe_get_value_from_dict(resp_data, 'id')
        return RpsResponse(
            id=id,
            type=safe_get_value_from_dict(data, 'type'),
            data=resp_data,
            issuer=RpsIssuer.from_dict(
                safe_get_value_from_dict(data, 'issuer')),
            createdAt=safe_get_value_from_dict(data, 'createdAt'),
        )

    @ staticmethod
    def from_response(response: RpsHookResponse | None):
        if response is None:
            return None

        if response.data is None:
            return None

        return RpsResponse.from_json(json.dumps(response.data))

    def __repr__(self):
        return self.to_json()
