# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

from typing import Tuple

from google.protobuf.any_pb2 import Any

from .. import logger
from ..notebook_library import run_notebook
from ..script_parameters import get_value_from_payload
from ..scripting_server_pb2 import RunWellKnownWorkflowRequest, RunWellKnownWorkflowResponse


def RunNotebook(payload: Any) -> Tuple[bool, Any, str]:
    logger.info(f"Run notebook request")
    request = RunWellKnownWorkflowRequest()
    payload.Unpack(request)

    parameters = None
    if request.parameters is not None:
        parameters = {}
        for item in request.parameters.dict.items():
            input = get_value_from_payload(item[1])
            if input[0]:
                if input[1] is not None:
                    var_name = item[0].lower().replace(" ", "_")
                    parameters[var_name] = input[1]

        logger.info(f"Parameters : {parameters}")

    output = run_notebook(request.workflow_id, parameters)
    if not output[0]:
        return (False, output[1])

    result = RunWellKnownWorkflowResponse()
    result.std_out = output[1]
    result.std_err = output[2]

    logger.info(f"Script executed successfully")
    return (True, result, "")
