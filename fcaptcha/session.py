import typing

from requests import Session, Response
from .exceptions import UnknownError
from .utils import check_exc, check_balance

import threading
import time

class Session(Session):
    """
    Base class for all FCaptcha requests.
    """
    BASE_URL: str = "https://api.fcaptcha.lol/api"
    TASK_PATH: str = "/createTask"
    VERIFY_PATH: str = "/getTaskData"

    def __init__(self, api_key: str) -> None:
        super().__init__()

        self.headers["authorization"]: str = api_key

        self.bal: threading.Thread = threading.Thread(
            target=self.run_bal_check,
            args=(api_key, 4)
        )
        self.bal.daemon: bool = True
        self.bal.start()

    def run_bal_check(self, key: str, sleep: int = 10) -> None:
        while True:
            check_balance(key)
            time.sleep(sleep)

    def make_request(
        self,
        action: str,
        method: str,
        json: typing.Dict[str, str],
        **kwargs: typing.Any
    ) -> Response:
        ACTIONS: typing.Dict[str, str] = {
            "verify": self.BASE_URL + self.VERIFY_PATH,
            "create": self.BASE_URL + self.TASK_PATH
        }
        URL: str = ACTIONS[action]

        try:
            response: Response = self.request(
                method=method,
                url=URL,
                json=json,
                **kwargs
            )
            return check_exc(response)
        except Exception as e:
            raise UnknownError(
                f"An unknown error has occured: {e}"
            )

    def add_data(
        self,
        payload: typing.Dict[str, str],
        rq_data: typing.Optional[str] = None,
        user_agent: typing.Optional[str] = None
    ) -> None:
        """
        Util function to add optional data to request payload.
        """
        if rq_data:
            payload["rqdata"] = rq_data

        if user_agent:
            payload["user_agent"] = user_agent

        return payload
