import logging
import os
from dataclasses import dataclass
from time import sleep
from typing import Any, Dict, Optional

import requests

from . import __version__, api, exceptions

log = logging.getLogger(__name__)

LATEST_API_VERSION = 2

CLEARNET_ENDPOINT = "https://api.sporestack.com"
TOR_ENDPOINT = (
    "http://api.spore64i5sofqlfz5gq2ju4msgzojjwifls7rok2cti624zyq3fcelad.onion"
)

API_ENDPOINT = CLEARNET_ENDPOINT

GET_TIMEOUT = 60
POST_TIMEOUT = 90
USE_TOR_PROXY = "auto"


session = requests.Session()


def _get_tor_proxy() -> str:
    """
    This makes testing easier.
    """
    return os.getenv("TOR_PROXY", "socks5h://127.0.0.1:9050")


# For requests module
TOR_PROXY_REQUESTS = {"http": _get_tor_proxy(), "https": _get_tor_proxy()}


def _is_onion_url(url: str) -> bool:
    """
    returns True/False depending on if a URL looks like a Tor hidden service
    (.onion) or not.
    This is designed to false as non-onion just to be on the safe-ish side,
    depending on your view point. It requires URLs like: http://domain.tld/,
    not http://domain.tld or domain.tld/.

    This can be optimized a lot.
    """
    try:
        url_parts = url.split("/")
        domain = url_parts[2]
        tld = domain.split(".")[-1]
        if tld == "onion":
            return True
    except Exception:
        pass
    return False


def _api_request(
    url: str,
    empty_post: bool = False,
    json_params: Optional[Dict[str, Any]] = None,
    retry: bool = False,
) -> Any:
    headers = {"User-Agent": f"sporestack-python/{__version__}"}
    proxies = {}
    if _is_onion_url(url) is True:
        log.debug("Got a .onion API endpoint, using local Tor SOCKS proxy.")
        proxies = TOR_PROXY_REQUESTS

    try:
        if empty_post is True:
            request = session.post(
                url, timeout=POST_TIMEOUT, proxies=proxies, headers=headers
            )
        elif json_params is None:
            request = session.get(
                url, timeout=GET_TIMEOUT, proxies=proxies, headers=headers
            )
        else:
            request = session.post(
                url,
                json=json_params,
                timeout=POST_TIMEOUT,
                proxies=proxies,
                headers=headers,
            )
    except Exception as e:
        if retry is True:
            log.warning(f"Got an error, but retrying: {e}")
            sleep(5)
            # Try again.
            return _api_request(
                url,
                empty_post=empty_post,
                json_params=json_params,
                retry=retry,
            )
        else:
            raise

    status_code_first_digit = request.status_code // 100
    if status_code_first_digit == 2:
        try:
            return request.json()
        except Exception:
            return request.content
    elif status_code_first_digit == 4:
        log.debug("HTTP status code: {request.status_code}")
        raise exceptions.SporeStackUserError(request.content.decode("utf-8"))
    elif status_code_first_digit == 5:
        if retry is True:
            log.warning(request.content.decode("utf-8"))
            log.warning("Got a 500, retrying in 5 seconds...")
            sleep(5)
            # Try again if we get a 500
            return _api_request(
                url,
                empty_post=empty_post,
                json_params=json_params,
                retry=retry,
            )
        else:
            raise exceptions.SporeStackServerError(str(request.content))
    else:
        # Not sure why we'd get this.
        request.raise_for_status()
        raise Exception("Stuff broke strangely. Please contact SporeStack support.")


@dataclass
class APIClient:
    api_endpoint: str = API_ENDPOINT

    def server_launch(
        self,
        machine_id: str,
        days: int,
        flavor: str,
        operating_system: str,
        ssh_key: str,
        token: str,
        region: Optional[str] = None,
        quote: bool = False,
        hostname: str = "",
        autorenew: bool = False,
    ) -> api.ServerLaunch.Response:
        request = api.ServerLaunch.Request(
            days=days,
            token=token,
            flavor=flavor,
            region=region,
            operating_system=operating_system,
            ssh_key=ssh_key,
            quote=quote,
            hostname=hostname,
            autorenew=autorenew,
        )
        url = self.api_endpoint + api.ServerLaunch.url.format(machine_id=machine_id)
        response = _api_request(url=url, json_params=request.dict())
        response_object = api.ServerLaunch.Response.parse_obj(response)
        assert response_object.machine_id == machine_id
        return response_object

    def server_topup(
        self,
        machine_id: str,
        days: int,
        token: str,
    ) -> api.ServerTopup.Response:
        """
        Topup a server.
        """
        request = api.ServerTopup.Request(days=days, token=token)
        url = self.api_endpoint + api.ServerTopup.url.format(machine_id=machine_id)
        response = _api_request(url=url, json_params=request.dict())
        response_object = api.ServerTopup.Response.parse_obj(response)
        assert response_object.machine_id == machine_id
        return response_object

    def autorenew_enable(self, machine_id: str) -> None:
        """
        Enable autorenew on a server.
        """
        url = self.api_endpoint + api.ServerEnableAutorenew.url.format(
            machine_id=machine_id
        )
        _api_request(url, empty_post=True)

    def autorenew_disable(self, machine_id: str) -> None:
        """
        Disable autorenew on a server.
        """
        url = self.api_endpoint + api.ServerDisableAutorenew.url.format(
            machine_id=machine_id
        )
        _api_request(url, empty_post=True)

    def server_start(self, machine_id: str) -> None:
        """
        Power on the server.
        """
        url = self.api_endpoint + api.ServerStart.url.format(machine_id=machine_id)
        _api_request(url, empty_post=True)

    def server_stop(self, machine_id: str) -> None:
        """
        Power off the server.
        """
        url = self.api_endpoint + api.ServerStop.url.format(machine_id=machine_id)
        _api_request(url, empty_post=True)

    def server_delete(self, machine_id: str) -> None:
        """
        Delete the server.
        """
        url = self.api_endpoint + api.ServerDelete.url.format(machine_id=machine_id)
        _api_request(url, empty_post=True)

    def server_forget(self, machine_id: str) -> None:
        """
        Forget about a destroyed/deleted server.
        """
        url = self.api_endpoint + api.ServerForget.url.format(machine_id=machine_id)
        _api_request(url, empty_post=True)

    def server_rebuild(self, machine_id: str) -> None:
        """
        Rebuilds the server with the operating system and SSH key set at launch time.

        Deletes all of the data on the server!
        """
        url = self.api_endpoint + api.ServerRebuild.url.format(machine_id=machine_id)
        _api_request(url, empty_post=True)

    def server_info(self, machine_id: str) -> api.ServerInfo.Response:
        """
        Returns info about the server.
        """
        url = self.api_endpoint + api.ServerInfo.url.format(machine_id=machine_id)
        response = _api_request(url)
        response_object = api.ServerInfo.Response.parse_obj(response)
        assert response_object.machine_id == machine_id
        return response_object

    def servers_launched_from_token(
        self, token: str
    ) -> api.ServersLaunchedFromToken.Response:
        """
        Returns info of servers launched from a given token.
        """
        url = self.api_endpoint + api.ServersLaunchedFromToken.url.format(token=token)
        response = _api_request(url)
        response_object = api.ServersLaunchedFromToken.Response.parse_obj(response)
        return response_object

    def flavors(self) -> api.Flavors.Response:
        """
        Returns available flavors.
        """
        url = self.api_endpoint + api.Flavors.url
        response = _api_request(url)
        response_object = api.Flavors.Response.parse_obj(response)
        return response_object

    def operating_systems(self) -> api.OperatingSystems.Response:
        """
        Returns available operating systems.
        """
        url = self.api_endpoint + api.OperatingSystems.url
        response = _api_request(url)
        response_object = api.OperatingSystems.Response.parse_obj(response)
        return response_object

    def token_add(
        self,
        token: str,
        dollars: int,
        currency: str,
        retry: bool = False,
    ) -> api.TokenAdd.Response:
        request = api.TokenAdd.Request(dollars=dollars, currency=currency)
        url = self.api_endpoint + api.TokenAdd.url.format(token=token)
        response = _api_request(url=url, json_params=request.dict(), retry=retry)
        response_object = api.TokenAdd.Response.parse_obj(response)
        assert response_object.token == token
        return response_object

    def token_balance(self, token: str) -> api.TokenBalance.Response:
        url = self.api_endpoint + api.TokenBalance.url.format(token=token)
        response = _api_request(url=url)
        response_object = api.TokenBalance.Response.parse_obj(response)
        assert response_object.token == token
        return response_object
