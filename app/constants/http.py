"""HTTP status codes (numeric literals for API layer)."""

from typing import Final

HTTP_200_OK: Final[int] = 200
HTTP_201_CREATED: Final[int] = 201
HTTP_400_BAD_REQUEST: Final[int] = 400
HTTP_401_UNAUTHORIZED: Final[int] = 401
HTTP_404_NOT_FOUND: Final[int] = 404
HTTP_422_UNPROCESSABLE_ENTITY: Final[int] = 422
HTTP_500_INTERNAL_SERVER_ERROR: Final[int] = 500
HTTP_503_SERVICE_UNAVAILABLE: Final[int] = 503
