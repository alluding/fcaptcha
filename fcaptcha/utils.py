from .exceptions import (
    InvalidAPIKey,
    InvalidJSON,
    TaskNotFound,
    UnknownError
)

from requests import Response
import typing


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
