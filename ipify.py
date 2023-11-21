"""Interact with the IPify REST API. For more information see https://www.ipify.org"""

from dataclasses import dataclass
import requests
import pydantic
import timestamp


class IPifyResponseModel(pydantic.BaseModel):
    """Response body from IPify"""
    ip: str


@dataclass
class IP:
    """Holds IP information"""
    ip: str


class IPify:  # pylint: disable=too-few-public-methods
    """Interact with the IPify REST API. For more information see https://www.ipify.org"""

    _IPIFY_API_ENDPOINT = "https://api.ipify.org/?format=json"

    def __init__(self, timeout: int = 10, verbose: bool = False):
        self.timeout = timeout
        self.verbose = verbose

    def get_current_ip(self) -> IP:
        """Get current IP address

        :return: Current IP address object
        """
        response = requests.get(
            url=self._IPIFY_API_ENDPOINT,
            timeout=self.timeout
        )
        if self.verbose:
            print(timestamp.get_timestamp(),
                  response.request.url, response.status_code)

        response.raise_for_status()

        parsed = IPifyResponseModel.model_validate_json(response.content)

        return IP(ip=parsed.ip)
