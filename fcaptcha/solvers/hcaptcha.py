from __future__ import annotations

from ..session import Session
from ..exceptions import InvalidArgs, TaskNotFound

import typing

if typing.TYPE_CHECKING:
    from typing_extensions import Self
    
class hCaptcha(Session):
    """
    Class for solving hCaptcha.
    """

    def __init__(self, api_key: str) -> None:
        super().__init__(api_key=api_key)
        
        self.task_id: str = None

    def create_task(
        self,
        site_key: str,
        host: str,
        proxy: str,
        **kwargs: typing.Any
    ) -> Self:
        if not all((proxy, site_key, host)):
            raise InvalidArgs(
                "You're missing one or more of the required arguments!"
            )

        payload: typing.Dict[str, str] = self.add_data(
            payload={
                "host": host,
                "sitekey": site_key,
                "proxy": proxy
            },
            rq_data=kwargs.get("rq_data"),
            user_agent=kwargs.get("user_agent")
        )

        response = self.make_request(
            action="create",
            method="post",
            json=payload
        ).json()["task"]

        self.task_id: str = response.get("task_id")

        return self

    def get_result(self) -> str:
        if not self.task_id:
            raise TaskNotFound("No task ID available. Create a task first.")

        while True:
            response = self.make_request(
                action="verify",
                method="get",
                json={"task_id": self.task_id}
            ).json()["task"]

            if response.get("state") == "processing":
                continue

            return response.get("captcha_key")
