from ..session import Session
from ..exceptions import InvalidArgs

import typing


class hCaptcha(Session):
    """
    Class for solving hCaptcha.
    """

    def __init__(self, api_key: str) -> None:
        super().__init__(api_key=api_key)

    def create_task(
        self,
        site_key: str,
        host: str,
        proxy: str,
        **kwargs: typing.Any
    ) -> str:
        if not proxy or site_key or host:
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

        return self.make_request(
            action="create",
            method="post",
            json=payload
        ).json()["task"].get("task_id")

    def task_result(self, task_id: str) -> str:
        while True:
            response = self.make_request(
                action="verify",
                method="get",
                json={"task_id": task_id}
            ).json()["task"]

            if response.get("state") == "processing":
                continue

            return response.get("captcha_key")
