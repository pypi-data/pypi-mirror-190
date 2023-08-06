import uuid

from rps_client.client import rps_service, rps_webhook
from rps_client.config import BASE_URL
from rps_client.info import (get_hostname, get_os_uname,
                  get_python_version, get_user_dir,
                  get_user_home)
from rps_client.models import RpsClientOptions, RpsHookRequest, RpsHookResponse, RpsIssuer, RpsResponse
from rps_client.utils import current_milli_time

from rps_client.logger import log


class RpsClient:
    NAME = 'rps-client'
    VERSION = '1.0.1'
    VERSION_CODE = "2"
    VERSION_DATE = "09-02-2023"
    SDK_TYPE = "python"

    def __init__(self, options: RpsClientOptions):
        self.id = str(uuid.uuid4())
        self.api_key = options.api_key
        self.base_url = options.base_url

        if self.api_key is None:
            raise ValueError("API Key is required")

        if self.base_url is None:
            self.base_url = BASE_URL

        # Init the SDK to service (Ping Service)
        self._bootstrap = self._get_bootstrap()
        log("Initialized Rps Client SDK id:", self.id, "version:",
            f"{self.VERSION}-{self.VERSION_CODE}", "via:", self.base_url, "with api-key:", self.api_key)

    def get_issuer(self) -> RpsIssuer | None:
        if self._bootstrap is None:
            return None

        return self._bootstrap.issuer

    def _get_bootstrap(self) -> RpsResponse:
        log("Bootstrapping RPS Client SDK to service...")
        uname = get_os_uname()
        data = {
            "instanceId": self.id,
            "startDate": current_milli_time(),
            "hostname": get_hostname(),
            "os": uname.system,
            "os.version": uname.release,
        }

        request = RpsHookRequest(
            type=None,
            data=data,
        )

        self._enhance_details(request)

        response = rps_service(
            request=request,
            api_key=self.api_key,
            base_url=self.base_url,
        )

        return RpsResponse.from_response(response)

    def _enhance_details(self, request: RpsHookRequest, retry: bool = False):
        # SDK Client
        request.add_details("sdk_id", self.id)
        request.add_details("sdk_name", self.NAME)
        request.add_details("sdk_version", self.VERSION)
        request.add_details("sdk_version_code", self.VERSION_CODE)
        request.add_details("sdk_version_date", self.VERSION_DATE)
        request.add_details("sdk_type", self.SDK_TYPE)

        # SDK Platform
        uname = get_os_uname()
        request.add_details("sdk_hostname", get_hostname())
        request.add_details("sdk_platform", uname.system)
        request.add_details("sdk_platform_version", uname.release)
        request.add_details("sdk_python_version", get_python_version())
        request.add_details("sdk_user_home", get_user_home())
        request.add_details("sdk_user_dir", get_user_dir())
        request.add_details("sdk_arch", uname.machine)

        if retry:
            request.add_details("rps_retry", True)
            request.add_send_at(current_milli_time())

    def send(self, request: RpsHookRequest) -> RpsHookResponse:
        self._enhance_details(request)

        response = rps_webhook(
            request=request,
            api_key=self.api_key,
            base_url=self.base_url,
        )

        return response
