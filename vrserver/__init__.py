#!/bin/env python3


import signal
import sys
import logging
import json

from flask import Flask
from flask import request
from flask.logging import default_handler
from flask import render_template

from vrserver.venv import Venv
from vrserver.dutmanager import DUTManager
from vrserver.util import APPError


class RequestFormatter(logging.Formatter):
    def format(self, record):
        # print(record)
        record.remote_addr = request.remote_addr
        record.url = request.url
        record.method = request.method
        record.data = request.get_json()
        return super(RequestFormatter, self).format(record)

FORMATTER = RequestFormatter(
    '[%(asctime)s][%(levelname)s] %(remote_addr)s %(method)s %(url)s %(data)s'
)
default_handler.setFormatter(FORMATTER)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    venv = Venv.start('127.0.0.1', 2000).proxy()

    @app.route('/ping', methods=['GET'])
    def ping():
        status = {}
        for sub_mode in [venv]:
            name = str(sub_mode.actor_ref.actor_class.__name__)
            try:
                status[name] = sub_mode.ping().get()
            except Exception as exp:
                print('EXP:', exp)
                status[name] = False
        status['http'] = True
        status['duts'] = DUTManager.dut_status()
        return json.dumps(status)

    @app.route('/scenario', methods=['GET', 'POST'])
    def scenario():
        if request.method == 'POST':
            return setup_scenario()
        else:
            return get_scenario_status()

    def setup_scenario():
        pass

    def get_scenario_status():
        pass

    @app.errorhandler(APPError)
    def handle_app_error(error):
        return (error.message, 404)

    @app.route('/scenario/dut/<dutname>', methods=['GET', 'POST', 'PUT'])
    def player(dutname):
        print(dutname)
        if request.method == 'POST':
            return set_dut(dutname, request.get_json())
        elif request.method == 'PUT':
            return change_dut(dutname, request.get_json())
        else:
            return get_dut_status(dutname)

    def set_dut(dutname, parameters):
        dut_type = None
        if "dut_type" in parameters:
            dut_type = parameters["dut_type"]
        autopilot = False
        if "autopilot" in parameters:
            autopilot = parameters["autopilot"]
        DUTManager.acquire_dut(dutname, venv, dut_type, autopilot)
        return '', 204

    def change_dut(dutname, parameters):
        DUTManager.change_dut(dutname, parameters)
        return '', 200


    def get_dut_status(dutname):
        return render_template('localdisplay.html', dutname=dutname)

    @app.route('/scenario/vehicle', methods=['GET', 'POST'])
    def vehicle():
        if request.method == 'POST':
            return set_vehicle()
        else:
            return get_vehicle_status()

    def set_vehicle():
        venv.acquire_vehicle_with_location().get()
        return '', 204

    def get_vehicle_status():
        pass

    @app.route('/scenario/pedestrian', methods=['GET', 'POST'])
    def pedestrian():
        if request.method == 'POST':
            return set_pedestrian()
        else:
            return get_pedestrian_status()

    def set_pedestrian():
        pass

    def get_pedestrian_status():
        pass

    return app
