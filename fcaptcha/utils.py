from .exceptions import (
    InvalidAPIKey,
    InvalidJSON,
    TaskNotFound,
    UnknownError,
    NoBalance
)

from requests import Response, get
import typing

def check_balance(key: str) -> str:
    response: typing.Dict[str, typing.Union[float, int]] = get(
        f"https://api.fcaptcha.lol/get_balance/{key}"
    ).json()
    balance: float | int = response.get("balance")

    if balance is None or balance <= 0:
        raise NoBalance(
            f"The key: {key} has no credits on FCaptcha!"
        )

    return balance

def check_exc(response: Response) -> typing.Dict[str, typing.Any]:
    ERROR_MAP: typing.Dict[str, typing.Union[InvalidAPIKey, InvalidJSON, TaskNotFound]] = {
        "Invalid JSON": InvalidJSON("The JSON data provided is improper. Please refer to the documentation for correct JSON formatting."),
        "Invalid API Key": InvalidAPIKey("The API key provided is invalid. Please check your key."),
        "Task not found": TaskNotFound("The task ID was not found. Please try creating a new task.")
    }

    error: str = response.json().get("error") if not isinstance(
        response.json().get("error"),
        bool
    ) else response.json().get("message")

    if error and error in ERROR_MAP:
        raise ERROR_MAP[error]

    return response
