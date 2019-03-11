#!/bin/env python3

import json

from vrserver.dut import DUT
from vrserver.util import DUTNotFoundError


class DUTManager(object):
    dut_dic = {}

    @staticmethod
    def acquire_dut(name, venv, dut_type=None, autopilot=False):
        if dut_type is None:
            dut_proxy = DUT.start(name, venv, autopilot).proxy()
            DUTManager.dut_dic[name] = dut_proxy

    @staticmethod
    def release_dut(name):
        if name in DUTManager.dut_dic:
            DUTManager.dut_dic[name].deactivate()
            DUTManager.dut_dic[name].destroy
            del DUTManager.dut_dic[name]

    @staticmethod
    def change_dut(name, parameters):
        if name not in DUTManager.dut_dic:
            raise DUTNotFoundError(name)
        DUTManager.dut_dic[name].control(parameters)

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
            status[name] = dut.get_status().get()
        return status
