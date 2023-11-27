"""Interact with the IPify REST API. For more information see https://www.ipify.org"""

import dataclasses
import retry
import requests
import pydantic
import utils


class IPifyResponseModel(pydantic.BaseModel):
    """Response body from IPify"""
    ip: str


@dataclasses.dataclass
class IP:
    """Holds IP information"""
    ip: str


class IPify(utils.Verbose):  # pylint: disable=too-few-public-methods
    """Interact with the IPify REST API. For more information see https://www.ipify.org"""

    _IPIFY_API_ENDPOINT = "https://api.ipify.org/?format=json"

    def __init__(self, timeout: int = 10, verbose: bool = False):
        self.timeout = timeout
        super().__init__(verbose)

    @retry.retry(exceptions=requests.Timeout, tries=2, delay=1)
    async def get_current_ip(self) -> IP:
        """Get current IP address

        :return: Current IP address object
        """
        response = requests.get(
            url=self._IPIFY_API_ENDPOINT,
            timeout=self.timeout
        )
        self.printer(f"{response.request.url} {response.status_code}")

        response.raise_for_status()

        parsed = IPifyResponseModel.model_validate_json(response.content)

        return IP(ip=parsed.ip)
