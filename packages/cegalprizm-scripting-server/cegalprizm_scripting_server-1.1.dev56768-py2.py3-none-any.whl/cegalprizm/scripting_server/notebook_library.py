# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

from typing import Dict, Iterator, List, NamedTuple, Tuple

import hashlib
import os
import json
import papermill as pm
import asyncio
import sys
from io import StringIO
import contextlib
from enum import Enum

from . import logger
from .script_library import compile_script
from .workflow_parameters import WorkflowInputTuple, get_workflow_input_parameter


class ScriptType(Enum):
    PyScript = 1
    Notebook = 2


class NotebookInfoTuple(NamedTuple):
    name: str
    category: str
    description: str
    authors: str
    version: str
    path: str
    type: ScriptType
    inputs: List[WorkflowInputTuple]


this = sys.modules[__name__]

this.environment_name: str = None
this.working_path: str = None
this.notebook_library_path: str = None
this.notebook_dict: Dict[str, NotebookInfoTuple] = {}


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


@contextlib.contextmanager
def stderrIO(stderr=None):
    old = sys.stderr
    if stderr is None:
        stderr = StringIO()
    sys.stderr = stderr
    yield stderr
    sys.stderr = old


def get_environment_name():
    return this.environment_name


def initialise_notebook_library(environment_name: str, notebook_library_path: str, working_path: str):
    if not os.path.exists(notebook_library_path):
        logger.warning(f'Specified library path not valid: {notebook_library_path}')
        return

    if not os.path.exists(working_path):
        logger.warning(f'Specified working directory not valid: {working_path}')
        return

    this.environment_name = environment_name
    this.working_path = working_path
    this.notebook_library_path = notebook_library_path

    logger.info(f"working_path: { this.working_path}")

    refresh_library()


def refresh_library():
    if this.notebook_library_path is None:
        return

    logger.info(f'Refreshing library: {this.notebook_library_path}')

    this.notebook_dict.clear()

    for filename in [f for f in os.listdir(this.notebook_library_path) if os.path.isfile(os.path.join(this.notebook_library_path, f))]:
        if filename.endswith(".json"):
            with open(os.path.join(this.notebook_library_path, filename), "r") as f:
                try:
                    data = json.load(f)
                    name: str = data["name"]
                    category: str = data["category"]
                    description: str = data["description"]
                    authors: str = data["authors"]
                    version: str = data["version"]
                    path: str = data["path"]
                    script_type = None
                    inputs = []

                    if path.startswith("./"):
                        path = os.path.join(this.notebook_library_path, path)

                    if os.path.isfile(path):
                        notebook_id = hashlib.md5(path.encode('utf-8')).hexdigest()
                        if notebook_id in this.notebook_dict.keys():
                            logger.debug(f"{filename} already defined")
                        else:
                            if path.endswith(".ipynb"):
                                script_type = ScriptType.Notebook
                            elif path.endswith(".py"):
                                script_type = ScriptType.PyScript
                            else:
                                logger.warning(f'Error adding {filename}: only .ipynb and .py files are supported')
                    else:
                        logger.warning(f'Error adding {filename}: path does not exist')

                    for key, item in data["inputs"].items():
                        inputs.append(get_workflow_input_parameter(key, item))

                    if script_type:
                        info = NotebookInfoTuple(name, category, description, authors, version, path, script_type, inputs)
                        logger.info(f'Add notebook: {name}')
                        this.notebook_dict[notebook_id] = info

                except Exception as err:
                    logger.debug(f"Unexpected {err=}, {type(err)=}")
                    logger.warning(f'Error reading file: {filename}')


def run_notebook(notebook_id: str, parameters) -> Tuple[bool, str]:
    try:
        if notebook_id not in this.notebook_dict.keys():
            logger.debug(f"Library  {notebook_id} does not exist")
            return (False, f"Notebook {notebook_id} does not exist")

        info = this.notebook_dict[notebook_id]

        logger.info(f"working_path: {this.working_path}")

        if info.type == ScriptType.Notebook:
            if os.name == 'nt':
                from asyncio import WindowsSelectorEventLoopPolicy
                asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())

            with stdoutIO() as stdout:
                with stderrIO() as stderr:
                    with pm.execute.chdir(this.working_path):
                        pm.execute_notebook(
                            input_path=info.path,
                            output_path="out.ipynb",
                            parameters=parameters,
                            log_output=True
                        )

                        return (True, stdout.getvalue(), stderr.getvalue())

        elif info.type == ScriptType.PyScript:
            with open(info.path, 'r') as file:
                script = file.read()
                parameters["working_path"] = this.working_path
                path = os.path.normpath(os.path.dirname(info.path)).replace('\\', '/')
                os.chdir(path)
                injected_code = f"import sys\nsys.path.append('{path}')\n"
                compile_result = compile_script(script, parameters, injected_code, False)
                if compile_result[0]:
                    return (True, compile_result[2], compile_result[3])
                else:
                    return (False, compile_result[3])

        else:
            logger.warning(f'{e}')
            return (False, f'Error running {info.name}')

    except Exception as e:
        logger.warning(f'{e}')
        return (False, f'Error running notebook')


def list_available_notebooks() -> Iterator[Tuple[str, NotebookInfoTuple]]:
    for key in this.notebook_dict.keys():
        yield (key, this.notebook_dict[key])


def get_notebook_info(notebook_id: str) -> NotebookInfoTuple:
    if notebook_id not in this.notebook_dict.keys():
        return None
    return this.notebook_dict[notebook_id]
