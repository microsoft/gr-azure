#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio Azure software radio module. Place your Python package
description here (python/__init__.py).
'''
import os

# import pybind11 generated symbols into the azure_software_radio namespace
try:
    # this might fail if the module is python-only
    from .azure_software_radio_python import *
except ModuleNotFoundError:
    pass

# import any pure python here
from .blob_qa_common import blob_teardown, blob_setup
from .blob_sink import BlobSink
from .blob_source import BlobSource
from . import blob_common
from .eventhub_sink import EventHubSink
from .eventhub_source import EventHubSource
from .rest_api import RestApi
