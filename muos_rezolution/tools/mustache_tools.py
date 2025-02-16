import json
import os
import re

import muos_rezolution.tools.display_tools as c

NOTFOUND_PLACEHOLDER = "##NOTFOUND##"
nf = NOTFOUND_PLACEHOLDER


def interpretAsJson(jsonString: str) -> dict:
    try:
        return json.loads(jsonString)
    except json.decoder.JSONDecodeError as error:
        c.error(f"Invalid JSON : {error.msg}")
        exit(os.EX_DATAERR)


def replaceMustaches(template: str, data: dict[str, str]) -> str:
    return re.sub('{{(.*?)}}', lambda match: str(data.get(match.group(1), nf)), template)
