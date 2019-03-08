#!/bin/env python2


import signal
import sys
import logging

from flask import Flask
from flask import request
from flask.logging import default_handler
from flask import render_template

from vrserver.venv import Venv
from vrserver.ctu import CTU
from vrserver.controller import Controller
from vrserver.util import PlayerNotFoundError
from vrserver.localdisplay import LocalDisplay


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
    ctu = CTU().start().proxy()
    ctr = Controller.start(venv, ctu).proxy()

    @app.route('/ping', methods=['GET'])
    def ping():
        status = {}
        for sub_mode in [venv, ctu, ctr]:
            name = str(sub_mode.actor_ref.actor_class.__name__)
            try:
                status[name] = sub_mode.ping().get()
            except Exception as exp:
                print('EXP:', exp)
                status[name] = False
        status['http'] = True
        return str(status)

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

    @app.errorhandler(PlayerNotFoundError)
    def handle_player_not_found(error):
        return (error.message, 404)

    @app.route('/scenario/player', methods=['GET', 'POST'])
    def player():
        if request.method == 'POST':
            return set_player(request.get_json())
        else:
            return get_player_status()

    def set_player(parameters):
        venv.set_player(
            vehicle_name='vehicle.lincoln.mkz2017',
            role_name='hero',
            color_id=0,
            position_id=0,
            autopilot=False).get()
        return '', 204

    def get_player_status():
        return venv.get_player_status().get()

    @app.route('/scenario/vehicle', methods=['GET', 'POST'])
    def vehicle():
        if request.method == 'POST':
            return set_vehicle()
        else:
            return get_vehicle_status()

    def set_vehicle():
        venv.set_vehicle(
            vehicle_name='vehicle.audi.tt',
            role_name='hero',
            color_id=0,
            position_id=0).get()
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

    @app.route('/localdisplay', methods=['GET'])
    def localdisplay():
        venv.add_listener(LocalDisplay()).get()
        return '', 204

    @app.route('/localdisplay_show', methods=['GET'])
    def localdisplay_show():
        return render_template('localdisplay.html')

    return app
