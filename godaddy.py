"""Interact with the GoDaddy REST API. For more information see https://developer.godaddy.com"""

from dataclasses import dataclass
import requests
import pydantic
import utils


class ARecordResponseModel(pydantic.BaseModel):
    """Domain A record response model"""
    data: str
    name: str
    ttl: int
    type: str


@dataclass
class ARecord:
    """Holds data for a domain's DNS A record"""
    ip: str
    ttl: int


class GoDaddy(utils.Verbose):
    """Interact with the GoDaddy REST API. For more information see https://developer.godaddy.com"""

    _GODADDY_API_ENDPOINT = "https://api.godaddy.com/v1/domains/{domain}/records/A/@"

    def __init__(self, api_key: str, api_secret: str, timeout: int = 10, verbose: bool = False):
        self.timeout = timeout
        self.headers = {
            "Authorization": f"sso-key {api_key}:{api_secret}",
            "Content-Type": "application/json"
        }
        super().__init__(verbose)

    def get_a_record(self, domain: str) -> ARecord:
        """Get a domain's DNS A record

        :param domain: Domain to get A record for
        :return: Domain A record object
        """
        response = requests.get(
            url=self._GODADDY_API_ENDPOINT.format(domain=domain),
            timeout=self.timeout,
            headers=self.headers
        )
        self.printer(f"{response.request.url} {response.status_code}")

        response.raise_for_status()

        parsed = pydantic.TypeAdapter(
            list[ARecordResponseModel]).validate_json(response.content)
        if len(parsed) == 0:
            raise ValueError(
                "No A records were found."
            )
        if not len(parsed) == 1:
            raise NotImplementedError(
                "More than one A record present. Multiple A records not currently supported."
            )

        a_record = ARecord(
            ip=parsed[0].data,
            ttl=parsed[0].ttl
        )

        return a_record

    def update_a_record(self, domain: str, ip: str, ttl: int = 600) -> None:
        """Update a domain DNS A record

        :param domain: Domain to update DNS A record for
        :param ip: IP address to set to
        :param ttl: DNS TTL, defaults to 600
        """
        response = requests.put(
            url=self._GODADDY_API_ENDPOINT.format(domain=domain),
            timeout=self.timeout,
            headers=self.headers,
            json=[
                {
                    "data": ip,
                    "ttl": ttl
                }
            ]
        )
        self.printer(f"{response.request.url} {response.status_code}")

        response.raise_for_status()
