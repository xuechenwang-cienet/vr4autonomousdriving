#!/bin/env python3

import datetime

from  vrserver.util import BaseActor
from vrserver.sensormanager import SensorManager


class DUT(BaseActor):
    __control_list = ['manual_gear_shift', 'gear', 'throttle', 'steer', 'brake', 'hand_brake', 'reverse']

    def __init__(self, name, venv, autopilot=False):
        super(DUT, self).__init__()
        self._name = name
        self._venv = venv

        self._player = None
        self._sensor_manager = None
        self._control = None
        self._acquire_player(autopilot)

    def __del__(self):
        self.destroy()

    def active(self):
        pass

    def deactivate(self):
        pass

    def get_name(self):
        return self._name

    def _acquire_player(self, autopilot=False):
        self._player = self._venv.acquire_vehicle_with_position_id(self._name).get()
        self._player.set_autopilot(autopilot)
        self._sensor_manager = SensorManager(self._player)
        self._control = self._player.get_control()

    def control(self, parameters):
        control = parameters
        some_diff = False
        for action in DUT.__control_list:
            if control[action] != self._control.__getattribute__(action):
                self._control.__setattr__(action, control[action])
                some_diff = True
        if some_diff is False:
            return
        self._player.apply_control(self._control)

    def get_status(self):
        status = self._sensor_manager.get_status(convert=True)
        status['player'] = {}
        transform = self._player.get_transform()
        status['player']['location_x'] = transform.location.x
        status['player']['location_y'] = transform.location.y
        status['player']['rotation_yaw'] = transform.rotation.yaw
        status['player']['control'] = {}
        for action in DUT.__control_list:
            status['player']['control'][action] = self._control.__getattribute__(action)
        return status

    def destroy(self):
        if self._player:
            self._player.destroy()
            self._player = None
        if self._sensor_manager:
            self._sensor_manager.destroy()
            self._sensor_manager = None
