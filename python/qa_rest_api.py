# pylint: disable=missing-function-docstring, no-self-use, missing-class-docstring, no-member, eval-used, unused-variable, attribute-defined-outside-init
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) Microsoft Corporation.
# Licensed under the GNU General Public License v3.0 or later.
# See License.txt in the project root for license information.
#

import ast
import time

from socket import socket
from fastapi import status
from gnuradio import gr_unittest

import httpx
from rest_api import RestApi


class QaRestApi(gr_unittest.TestCase):

    def get_free_port(self):
        with socket() as sock:
            sock.bind(('', 0))
            return sock.getsockname()[1]

    def test_instance(self):
        port = self.get_free_port()
        instance = RestApi(self, port)
        self.assertIsNotNone(instance)

    def set_var1(self, val):
        self.var1 = val

    def set_var2(self, val):
        self.var2 = val

    def test_get_status(self):
        self.check_var1 = 1
        self.check_var2 = '2'
        self.check_var3 = {'pi': 3.14}
        port = self.get_free_port()
        instance = RestApi(self, port, read_settings=['check_var1', 'check_var2', 'check_var3'])
        time.sleep(1)
        addr_str = 'http://127.0.0.1:' + str(port) + '/status'
        resp = httpx.Client().get(addr_str)
        self.assertIsNotNone(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        dict_str = resp.content.decode("UTF-8")
        for i in range(1, 4):
            check_str = f'check_var{i}'
            self.assertEqual(check_str in dict_str, True)
        self.assertEqual('fake_var' in dict_str, False)

    def test_config_by_name(self):
        self.var1 = None
        self.var2 = None
        port = self.get_free_port()
        instance = RestApi(self, port, write_settings=['var1', 'var2'])
        # give server a second to startup
        time.sleep(1)
        self.var1 = 0
        self.var2 = 0
        addr_str = 'http://127.0.0.1:' + str(port) + '/config'
        resp = httpx.Client().put(addr_str, json={"var1": 3.14, "var2": 5.0})
        self.assertIsNotNone(resp)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(self.var1, 3.14)
        self.assertEqual(self.var2, 5.0)

    def test_bad_config_by_name(self):
        self.var1 = None
        port = self.get_free_port()
        instance = RestApi(self, port, write_settings=['var1'])
        # give server a second to startup
        time.sleep(1)
        self.var1 = 0
        addr_str = 'http://127.0.0.1:' + str(port) + '/config'
        resp = httpx.Client().put(addr_str, json={"var2":3.14}) # request a var/param that wasnt exposed
        self.assertIsNotNone(resp)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

if __name__ == '__main__':
    gr_unittest.run(QaRestApi)
