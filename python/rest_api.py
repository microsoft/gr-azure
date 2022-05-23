#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) Microsoft Corporation.
# Licensed under the GNU General Public License v3.0 or later.
# See License.txt in the project root for license information.
#
# pylint: disable=no-member, abstract-method, broad-except, unused-variable
#

import threading

from typing import List
from fastapi import FastAPI
from fastapi import HTTPException, status
from gnuradio import gr

import uvicorn


class RestApi(gr.basic_block):
    """
    See the yaml file for usage docs
    """

    def __init__(self, tbself, port, read_settings: List[str] = None, write_settings: List[str] = None):
        gr.basic_block.__init__(self,
                                name="rest_api",
                                in_sig=[],
                                out_sig=[])
        app = FastAPI()

        @app.get("/status")
        def get_status():
            """
            Get the block's readable status settings
            """
            all_settings = dir(tbself)

            if not read_settings:
                return {}

            read_status = {}
            for name in read_settings:
                if name in all_settings:
                    read_status[name] = getattr(tbself, name)
            return read_status

        @app.put("/config")
        def call_by_name(callbacks: dict):
            """
            Executes a callable/writable function in the top block
            """
            if not write_settings:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail={'Error': f'No writable settings were provided.'})

            for name in callbacks:
                setter_name = "set_" + name
                if name not in write_settings:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail={'Error': f'Function {setter_name} is not a writeable/callable.'})
                try:
                    # Get the setter that GNU Radio created for that variable, and call it with the new value
                    func = getattr(tbself, setter_name)
                    func(callbacks[name])
                except Exception:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail={'Error': f'Failed to call {setter_name}.'})

        self.server_thread = threading.Thread(
            target=uvicorn.run, args=(app,), kwargs={'port': port}, daemon=True)
        self.server_thread.start()
