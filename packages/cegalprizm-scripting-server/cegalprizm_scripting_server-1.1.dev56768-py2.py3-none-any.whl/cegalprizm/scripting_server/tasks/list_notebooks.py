# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

from typing import Tuple

from google.protobuf.any_pb2 import Any

from .. import logger
from ..notebook_library import get_environment_name, list_available_notebooks, refresh_library
from ..scripting_server_pb2 import WellKnownWorkflow, ListWellKnownWorkflowsRequest, ListWellKnownWorkflowsResponse
from ..workflow_parameters import get_wellknown_workflow_input


def ListNotebooks(payload: Any) -> Tuple[bool, Any, str]:
    logger.info(f"List notebooks request")
    request = ListWellKnownWorkflowsRequest()
    payload.Unpack(request)

    result = ListWellKnownWorkflowsResponse()

    refresh_library()

    for notebook_tuple in list_available_notebooks():
        item = WellKnownWorkflow()
        item.environment_name = get_environment_name()
        item.workflow_id = notebook_tuple[0]
        item.name = notebook_tuple[1].name
        item.category = notebook_tuple[1].category
        item.description = notebook_tuple[1].description
        item.authors = notebook_tuple[1].authors
        item.version = notebook_tuple[1].version
        for parameter in notebook_tuple[1].inputs:
            item.inputs.append(get_wellknown_workflow_input(parameter))

        result.workflows.append(item)

    logger.info(f"List notebooks successful")
    return (True, result, "")
