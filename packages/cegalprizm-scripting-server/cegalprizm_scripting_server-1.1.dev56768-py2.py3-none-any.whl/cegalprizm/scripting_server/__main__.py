# Copyright 2022 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

import os
import logging
from time import gmtime, strftime
import uuid
from packaging import version

from cegalprizm.hub import HubConnector

from . import __version__, logger
from .in_memory_token_provider import InMemoryTokenProvider
from .notebook_library import initialise_notebook_library
from .task_registry import get_task_registry

import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--name', help='Name to be assigned to the scripting environment', required=True, default='python')
parser.add_argument('--logdir', help='Path to directory in which to write the logfile', required=False)
parser.add_argument('--loglevel', help='Level of logging [debug, info, warning, error]', required=False, default='warning')
parser.add_argument('--workflow_library_path', help='Path to directory in which available workflows are described', required=False)
parser.add_argument('--working_dir_path', help='Path to working directory to be used when running workflows', required=False)

args = parser.parse_args()

scripting_uuid = uuid.uuid4()

if args.loglevel.startswith('debug'):
    level = logging.DEBUG
elif args.loglevel.startswith('warning'):
    level = logging.WARNING
elif args.loglevel.startswith('error'):
    level = logging.ERROR
else:
    level = logging.INFO

if args.logdir is not None:
    if not os.path.isdir(args.logdir):
        print("Error: Specified logdir does not exist")
        exit(0)

    filename = f"scripting-server_{strftime('%Y-%m-%d_%H-%M-%S', gmtime())}_{scripting_uuid}.log"

    logging.basicConfig(
        handlers=[logging.FileHandler(filename=os.path.join(args.logdir, filename), encoding='utf-8', mode='a+')],
        format='%(asctime)s [%(levelname)-8s] %(message)s',
        level=level,
        datefmt='%Y-%m-%d %H:%M:%S')
else:
    logging.basicConfig(level=level)

token_provider = None
join_token = ""
supports_public_requests = True

try:
    join_token = os.environ["CEGAL_HUB_CONNECTOR_JOIN_TOKEN"]
    supports_public_requests = True
except:
    join_token = ""

try:
    access_token = os.environ["CEGAL_HUB_ACCESS_TOKEN"]
    token_provider = InMemoryTokenProvider(access_token)
    supports_public_requests = False
    join_token = ""
except:
    token_provider = None
    join_token = ""

try:
    ver = version.parse(__version__)
    ver.major
except AttributeError:
    logger.info(f"cannot parse major version, you are probably running a development version")
    ver = version.parse("0.0.1")

logging.getLogger("cegalprizm.keystone_auth").setLevel(level)
logging.getLogger("cegalprizm.hub").setLevel(level)

logger.info(f"Starting Scripting Server {str(ver)}")

if args.workflow_library_path is not None:
    initialise_notebook_library(args.name, args.workflow_library_path.replace("\\", "/"), args.working_dir_path.replace("\\", "/"))

labels = {
    "scripting-environment": args.name,
    "scripting-uuid": str(scripting_uuid)
}

connector = HubConnector(wellknown_identifier="cegal.scripting_server",
                         friendly_name="Cegal Scripting Server",
                         description="A Cegal provided server allowing python code to be executed remotely using Cegal Hub",
                         version=str(ver),
                         build_version="local",
                         supports_public_requests=supports_public_requests,
                         join_token=join_token,
                         token_provider=token_provider,
                         additional_labels=labels)

connector.start(get_task_registry())
