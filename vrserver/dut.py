#!/bin/env python3

import datetime

from  vrserver.util import BaseActor
from vrserver.sensormanager import SensorManager


class DUT(BaseActor):
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
        print(control)
        if 'manual_gear_shift' in control:
            self._control.manual_gear_shift = control['manual_gear_shift']
        if 'gear' in control:
            self._control.gear = control['gear']
        if 'throttle' in control:
            self._control.throttle = control['throttle']
        if 'steer' in control:
            self._control.steer =control['steer']
        if 'brake' in control:
            self._control.brake = control['brake']
        if 'hand_brake' in control:
            self._control.hand_brake = control['hand_brake']

    def get_status(self):
        status = self._sensor_manager.get_status(convert=True)
        status['player'] = {}
        transform = self._player.get_transform()
        status['player']['location_x'] = transform.location.x
        status['player']['location_y'] = transform.location.y
        status['player']['rotation_yaw'] = transform.rotation.yaw
        status['player']['control'] = {}
        status['player']['control']['manual_gear_shift'] = self._control.manual_gear_shift
        status['player']['control']['gear'] = self._control.gear
        status['player']['control']['throttle'] = self._control.throttle
        status['player']['control']['steer'] = self._control.steer
        status['player']['control']['brake'] = self._control.brake
        status['player']['control']['hand_brake'] = self._control.hand_brake
        return status

    def destroy(self):
        if self._player:
            self._player.destroy()
            self._player = None
        if self._sensor_manager:
            self._sensor_manager.destroy()
            self._sensor_manager = None
