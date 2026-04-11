from typing import Annotated

from fastapi import APIRouter, Path

from app.constants import auth as auth_c
from app.constants import messages as msg_c
from app.services import catalog_service

router = APIRouter(prefix=auth_c.ROUTER_PREFIX_CATALOGS, tags=[auth_c.ROUTER_TAG_CATALOGS])


@router.get(auth_c.ROUTE_CATALOGS_MODIFIABLE_VARIABLES)
def list_modifiable_variables() -> dict:
    return {msg_c.KEY_DATA: catalog_service.get_modifiable_variables_catalog()}


@router.get(auth_c.ROUTE_CATALOGS_FIELD)
def get_catalog_field(
    field: Annotated[str, Path(description="Nombre del campo (snake_case)")],
) -> dict:
    return {msg_c.KEY_DATA: catalog_service.get_catalog_by_field(field)}
