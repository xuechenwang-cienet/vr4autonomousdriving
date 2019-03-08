#!/bin/env python2

from  vrserver.sensorlistener import SensorListener
from vrserver.sensormanager import SensorManager


class DUT(SensorListener):
    def __init__(self, name, venv):
        super(DUT, self).__init__()
        self._name = name
        self._venv = venv
        self._player = None
        self._sensor_manager = None
        self._acquire_player()

    def __del__(self):
        self.destroy()

    def active(self):
        pass

    def deactivate(self):
        pass

    def get_name(self):
        return self._name

    # SensorListener
    def on_gnss_event(self, gnss_event):
        pass

    # SensorListener
    def on_camera_rgb_event(self, image):
        pass

    def _acquire_player(self):
        self._player = self._venv.acquire_vehicle_with_position_id(self._name).get()

        self._player.set_autopilot(False)

        self._sensor_manager = SensorManager()
        self._sensor_manager.add_parent_actor(self._player)

    def destroy(self):
        if self._player:
            self._player.destroy()
            self._player = None
        if self._sensor_manager:
            self._sensor_manager.destroy()
            self._sensor_manager = None
