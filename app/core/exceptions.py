"""API errors shaped like docs/api-contracts.md (error envelope)."""

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.constants import http as http_c
from app.constants import messages as msg_c


class APIError(Exception):
    def __init__(
        self,
        status_code: int,
        *,
        code: str,
        message: str,
        details: dict | None = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


async def api_error_handler(_request: Request, exc: APIError) -> JSONResponse:
    body: dict = {
        msg_c.KEY_ERROR: {
            msg_c.KEY_CODE: exc.code,
            msg_c.KEY_MESSAGE: exc.message,
        }
    }
    if exc.details is not None:
        body[msg_c.KEY_ERROR][msg_c.KEY_DETAILS] = exc.details
    return JSONResponse(status_code=exc.status_code, content=body)


async def validation_error_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    errs = exc.errors()
    first = errs[0] if errs else {}
    loc = first.get("loc", ())
    field = str(loc[-1]) if loc else msg_c.FIELD_BODY
    return JSONResponse(
        status_code=http_c.HTTP_400_BAD_REQUEST,
        content={
            msg_c.KEY_ERROR: {
                msg_c.KEY_CODE: msg_c.ERROR_CODE_VALIDATION,
                msg_c.KEY_MESSAGE: msg_c.MSG_VALIDATION_FAILED,
                msg_c.KEY_DETAILS: {
                    msg_c.KEY_FIELD: field,
                    msg_c.KEY_REASON: first.get("msg", msg_c.MSG_VALIDATION_INVALID_INPUT),
                },
            }
        },
    )
