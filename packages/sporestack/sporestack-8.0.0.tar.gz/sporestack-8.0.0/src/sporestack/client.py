from dataclasses import dataclass
from typing import List, Union

from . import api
from .api_client import APIClient
from .utils import random_machine_id, random_token


@dataclass
class Server:
    machine_id: str
    api_client: APIClient = APIClient()
    token: Union[str, None] = None

    def info(self) -> api.ServerInfo.Response:
        return self.api_client.server_info(self.machine_id)

    def rebuild(self) -> None:
        self.api_client.server_rebuild(self.machine_id)

    def forget(self) -> None:
        self.api_client.server_forget(self.machine_id)

    def delete(self) -> None:
        self.api_client.server_delete(self.machine_id)

    def start(self) -> None:
        """Powers on the server."""
        self.api_client.server_start(self.machine_id)

    def stop(self) -> None:
        """Powers off the server."""
        self.api_client.server_stop(self.machine_id)

    def autorenew_enable(self) -> None:
        """Enables autorenew on the server."""
        self.api_client.autorenew_enable(self.machine_id)

    def autorenew_disable(self) -> None:
        """Disables autorenew on the server."""
        self.api_client.autorenew_disable(self.machine_id)

    def topup(self, days: int) -> None:
        """
        Renew the server for the amount of days specified, from the token specified.
        """
        if self.token is None:
            raise ValueError("token must be set to top up a server!")
        self.api_client.server_topup(
            machine_id=self.machine_id, days=days, token=self.token
        )


@dataclass
class Token:
    token: str = random_token()
    api_client: APIClient = APIClient()

    def add(self, dollars: int, currency: str) -> None:
        """Add to token"""
        self.api_client.token_add(token=self.token, dollars=dollars, currency=currency)

    def balance(self) -> int:
        """Returns the token's balance in cents."""
        return self.api_client.token_balance(token=self.token).cents

    def servers(self) -> List[Server]:
        server_classes: List[Server] = []
        for server in self.api_client.servers_launched_from_token(self.token).servers:
            server_classes.append(
                Server(
                    machine_id=server.machine_id,
                    api_client=self.api_client,
                    token=self.token,
                )
            )
        return server_classes

    def launch_server(
        self,
        ssh_key: str,
        flavor: str,
        days: int,
        operating_system: str,
        region: Union[str, None] = None,
        hostname: str = "",
        autorenew: bool = False,
        machine_id: str = random_machine_id(),
    ) -> Server:
        self.api_client.server_launch(
            machine_id=machine_id,
            days=days,
            token=self.token,
            region=region,
            flavor=flavor,
            operating_system=operating_system,
            ssh_key=ssh_key,
            hostname=hostname,
            autorenew=autorenew,
        )
        return Server(
            machine_id=machine_id, api_client=self.api_client, token=self.token
        )
