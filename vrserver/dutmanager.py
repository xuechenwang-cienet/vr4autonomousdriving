#!/bin/env python2

import json

from vrserver.dut import DUT
from vrserver.util import DUTNotFoundError


class DUTManager(object):
    dut_dic = {}

    @staticmethod
    def acquire_dut(name, venv, dut_type=None):
        if dut_type is None:
            DUTManager.dut_dic[name] = DUT(name, venv)

    @staticmethod
    def release_dut(name):
        if name in DUTManager.dut_dic:
            DUTManager.dut_dic[name].deactivate()
            DUTManager.dut_dic[name].destroy
            del DUTManager.dut_dic[name]

    @staticmethod
    def active_dut(name):
        if name not in DUTManager.dut_dic:
            raise DUTNotFoundError(name)
        DUTManager.dut_dic[name].active()

    @staticmethod
    def deactivate_dut(name):
        if name not in DUTManager.dut_dic:
            raise DUTNotFoundError(name)
        DUTManager.dut_dic[name].deactivate()

    @staticmethod
    def dut_status():
        status = {}
        for name, dut in DUTManager.dut_dic.items():
            status[name] = dut.ping().get()
        return status
