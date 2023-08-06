# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

from typing import List, NamedTuple

from cegalprizm.scripting_server.scripting_server_pb2 import BooleanWorkflowInput, IntegerWorkflowInput, DoubleWorkflowInput, StringWorkflowInput, EnumWorkflowInput, ObjectRefWorkflowInput, WellKnownWorkflowInput


class WorkflowInputTuple(NamedTuple):
    name: str
    type: str
    description: str


class BooleanWorkflowInputTuple(WorkflowInputTuple):
    default_value: bool = None

    def __new__(cls, name: str, type: str, description: str, default_value: bool):
        self = super(BooleanWorkflowInputTuple, cls).__new__(cls, name, type, description)
        self.default_value = default_value
        return self


class IntegerWorkflowInputTuple(WorkflowInputTuple):
    default_value: int = None
    minimum_value: int = None
    maximum_value: int = None

    def __new__(cls, name: str, type: str, description: str, default_value: int, minimum_value: int, maximum_value: int):
        self = super(IntegerWorkflowInputTuple, cls).__new__(cls, name, type, description)
        self.default_value = default_value
        self.minimum_value = minimum_value
        self.maximum_value = maximum_value
        return self


class DoubleWorkflowInputTuple(WorkflowInputTuple):
    default_value: float = None
    minimum_value: float = None
    maximum_value: float = None
    measurement_name: str = None
    display_symbol: str = None

    def __new__(cls, name: str, type: str, description: str, default_value: float, minimum_value: float, maximum_value: float, measurement_name: str, display_symbol: str):
        self = super(DoubleWorkflowInputTuple, cls).__new__(cls, name, type, description)
        self.default_value = default_value
        self.minimum_value = minimum_value
        self.maximum_value = maximum_value
        self.measurement_name = measurement_name
        self.display_symbol = display_symbol
        return self


class StringWorkflowInputTuple(WorkflowInputTuple):
    default_value: bool = None

    def __new__(cls, name: str, type: str, description: str, default_value: bool):
        self = super(StringWorkflowInputTuple, cls).__new__(cls, name, type, description)
        self.default_value = default_value
        return self


class EnumOptionTuple(NamedTuple):
    value: int
    name: str


class EnumWorkflowInputTuple(WorkflowInputTuple):
    default_value: int = None
    options: List[EnumOptionTuple]


class ObjectRefWorkflowInputTuple(WorkflowInputTuple):
    object_name: str = None
    property_name: str = None
    measurement_name: str = None
    linked_input_name: str = None

    def __new__(cls, name: str, type: str, description: str, object_name: str, property_name: str, measurement_name: str, linked_input_name: str):
        self = super(ObjectRefWorkflowInputTuple, cls).__new__(cls, name, type, description)
        self.object_name = object_name
        self.property_name = property_name
        self.measurement_name = measurement_name
        self.linked_input_name = linked_input_name
        return self


def get_workflow_input_parameter(key, item):
    if item["type"] == "bool":
        return BooleanWorkflowInputTuple(name=key,
                                         type="bool",
                                         description=item.get("description", ""),
                                         default_value=item.get("default_value", False))
    elif item["type"] == "int":
        return IntegerWorkflowInputTuple(name=key,
                                         type="int",
                                         description=item.get("description", ""),
                                         default_value=item.get("default_value", 0),
                                         minimum_value=item.get("minimum", 0),
                                         maximum_value=item.get("maximum", 0))
    elif item["type"] == "double":
        return DoubleWorkflowInputTuple(name=key,
                                        type="double",
                                        description=item.get("description", ""),
                                        default_value=item.get("default_value", 0),
                                        minimum_value=item.get("minimum", 0),
                                        maximum_value=item.get("maximum", 0),
                                        measurement_name=item.get("measurement_name", ""),
                                        display_symbol=item.get("display_symbol", ""))
    elif item["type"] == "string":
        return StringWorkflowInputTuple(name=key,
                                        type="string",
                                        description=item.get("description", ""),
                                        default_value=item.get("default_value", ""))
    elif item["type"] == "folder":
        return WorkflowInputTuple(name=key,
                                  type="folder",
                                  description=item.get("description", ""))
    elif item["type"] == "enum":
        return EnumWorkflowInputTuple(name=key,
                                      type="enum",
                                      description=item.get("description", ""))
    elif item["type"] == "object_ref":
        return ObjectRefWorkflowInputTuple(name=key,
                                           type="object_ref",
                                           description=item.get("description", ""),
                                           object_name=item.get("object_name", ""),
                                           property_name=item.get("property_name", ""),
                                           measurement_name=item.get("measurement_name", ""),
                                           linked_input_name=item.get("linked_input_name", ""))
    else:
        raise RuntimeWarning(f'Unsupported input["type"]: "{item["type"]}"')


def get_wellknown_workflow_input(parameter: WorkflowInputTuple):
    input = WellKnownWorkflowInput()
    input.name = parameter.name
    input.type = parameter.type
    input.description = parameter.description
    if (isinstance(parameter, BooleanWorkflowInputTuple)):
        input.boolean_input.default_value = parameter.default_value
    elif (isinstance(parameter, IntegerWorkflowInputTuple)):
        input.int_input.default_value = parameter.default_value
        input.int_input.minimum = parameter.minimum_value
        input.int_input.maximum = parameter.maximum_value
    elif (isinstance(parameter, DoubleWorkflowInputTuple)):
        print(parameter.measurement_name)
        input.double_input.default_value = parameter.default_value
        input.double_input.minimum = parameter.minimum_value
        input.double_input.maximum = parameter.maximum_value
        input.double_input.measurement_name = parameter.measurement_name
        input.double_input.display_symbol = parameter.display_symbol
    elif (isinstance(parameter, StringWorkflowInputTuple)):
        input.string_input.default_value = parameter.default_value
    # elif (isinstance(parameter, EnumWorkflowInputTuple)):
    #     input. enum_input = EnumWorkflowInput()
    elif (isinstance(parameter, ObjectRefWorkflowInputTuple)):
        input.object_ref_input.object_name = parameter.object_name
        input.object_ref_input.property_name = parameter.property_name
        input.object_ref_input.measurement_name = parameter.measurement_name
        input.object_ref_input.linked_input_name = parameter.linked_input_name
    return input
