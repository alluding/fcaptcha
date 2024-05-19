from __future__ import annotations
import typing
import time

from ..session import Session
from ..exceptions import InvalidArgs, TaskNotFound

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
        """
        Create a hCaptcha solving task.

        Args:
            site_key (str): The hCaptcha site key for the task.
            host (str): The host of the site for the task.
            proxy (str): The proxy for the task.
            **kwargs: Optional arguments for creating a task, including `rq_data`, and `user_agent`.

        Returns:
            Self: The instance of the hCaptcha solver. (allows chaining of `get_result` after creating task)
        
        Raises:
            InvalidArgs: If one or more required arguments are missing.
        """
    
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

    def get_result(self, sleep: typing.Optional[int] = 3) -> str:
        """
        Get the result of the hCaptcha solving task.

        Args:
            sleep (int, optional): The sleep interval in seconds between result checks. Defaults to 3.

        Returns:
            str: The solved hCaptcha key.

        Raises:
            TaskNotFound: If no task ID is available. Create a task first.
        """
        
        if not self.task_id:
            raise TaskNotFound("No task ID available. Create a task first.")

        while True:
            time.sleep(sleep)
            
            response = self.make_request(
                action="verify",
                method="get",
                json={"task_id": self.task_id}
            ).json()["task"]

            if response.get("state") == "processing":
                continue

            return response.get("captcha_key")
