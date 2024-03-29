"""Interact with the GoDaddy REST API. For more information see https://developer.godaddy.com"""

import dataclasses
import logging

import pydantic
import requests

logger = logging.getLogger(__name__)


class ARecordResponseModel(pydantic.BaseModel):
    """Domain A record response model"""

    data: str
    name: str
    ttl: int
    type: str


@dataclasses.dataclass
class ARecord:
    """Holds data for a domain's DNS A record"""

    ip: str
    ttl: int


class GoDaddy:
    """Interact with the GoDaddy REST API. For more information see https://developer.godaddy.com"""

    _GODADDY_API_ENDPOINT = "https://api.godaddy.com/v1/domains/{domain}/records/A/@"

    def __init__(self, api_key: str, api_secret: str, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            "Authorization": f"sso-key {api_key}:{api_secret}",
            "Content-Type": "application/json",
        }

    def get_a_record(self, domain: str) -> ARecord:
        """Get a domain's DNS A record

        :param domain: Domain to get A record for
        :return: Domain A record object
        """
        response = requests.get(
            url=self._GODADDY_API_ENDPOINT.format(domain=domain),
            timeout=self.timeout,
            headers=self.headers,
        )
        logger.debug(
            "Request URL: %s, Status Code: %d",
            response.request.url,
            response.status_code,
        )

        response.raise_for_status()

        parsed = pydantic.TypeAdapter(list[ARecordResponseModel]).validate_json(
            response.content
        )
        if len(parsed) == 0:
            raise ValueError("No A records were found.")
        if len(parsed) != 1:
            raise NotImplementedError(
                "More than one A record present. Multiple A records not currently supported."
            )

        a_record = ARecord(ip=parsed[0].data, ttl=parsed[0].ttl)

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
            json=[{"data": ip, "ttl": ttl}],
        )
        logger.debug(
            "Request URL: %s, Status Code: %d",
            response.request.url,
            response.status_code,
        )

        response.raise_for_status()
