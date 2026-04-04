"""Build catalog payloads from constants (allowed values, what-if metadata)."""

import copy

from app.constants import catalog as cat_c
from app.constants import http as http_c
from app.constants import messages as msg_c
from app.core.exceptions import APIError


def get_catalog_by_field(field: str) -> dict:
    if field not in cat_c.CATALOG_SUPPORTED_FIELDS:
        raise APIError(
            http_c.HTTP_404_NOT_FOUND,
            code=msg_c.ERROR_CODE_CATALOG_FIELD_NOT_SUPPORTED,
            message=msg_c.MSG_CATALOG_FIELD_NOT_SUPPORTED,
            details={
                msg_c.KEY_FIELD: field,
                msg_c.KEY_REASON: msg_c.MSG_CATALOG_UNSUPPORTED_FIELD_REASON,
            },
        )
    return {
        cat_c.KEY_FIELD: field,
        cat_c.KEY_DESCRIPTION: cat_c.CATALOG_FIELD_DESCRIPTIONS[field],
        cat_c.KEY_ALLOWED_VALUES: list(cat_c.CATALOG_FIELD_ALLOWED_VALUES[field]),
    }


def get_modifiable_variables_catalog() -> dict:
    modifiable = []
    for name in cat_c.MODIFIABLE_FIELDS_ORDER:
        spec = copy.deepcopy(cat_c.MODIFIABLE_VARIABLE_SPECS[name])
        entry = {cat_c.KEY_NAME: name, **spec}
        modifiable.append(entry)
    fixed = [
        {cat_c.KEY_NAME: name, cat_c.KEY_DESCRIPTION: desc}
        for name, desc in cat_c.FIXED_VARIABLE_ENTRIES
    ]
    return {
        cat_c.KEY_MODIFIABLE_VARIABLES: modifiable,
        cat_c.KEY_FIXED_VARIABLES: fixed,
    }
