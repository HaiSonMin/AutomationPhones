from typing import Any, Type


class IResponse(Type):
    message: str
    statusCode: int
    result: Any
    reasonStatusCode: str
