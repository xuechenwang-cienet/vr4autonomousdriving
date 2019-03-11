#!/bin/env python3

import weakref
import numpy as np
import base64
import cv2

import carla

from vrserver.sensor.gnsssensor import GnssSensor
from vrserver.sensor.rgbcamerasensor import RGBCameraSensor

class SensorManager(object):
    def __init__(self, parent_actor):
        self._parent = parent_actor

        self._gnss_sensor = GnssSensor(self._parent)
        self._camera_rgb_sensor = RGBCameraSensor(self._parent)
        self._lidar_sensor = None

    def destroy(self):
        for actor in [self._gnss_sensor, self._camera_rgb_sensor, self._lidar_sensor]:
            if actor is not None:
                actor.destroy()
    
    def __del__(self):
        self.destroy()

    def get_status(self, convert=False):
        status = {}
        status['camera_rgb'] = {}
        status['camera_rgb']['image'] = self._camera_rgb_sensor.camera_rgb
        status['camera_rgb']['type'] = 'raw'
        status['camera_rgb']['timestamp'] = str(self._camera_rgb_sensor.timestamp)
        status['gnss'] = {}
        status['gnss']['lat'] = self._gnss_sensor.lat
        status['gnss']['lon'] = self._gnss_sensor.lon
        status['gnss']['timestamp'] = str(self._gnss_sensor.timestamp)

        if convert and status['camera_rgb']['image'] is not None:
            raw_image = status['camera_rgb']['image'].copy()
            _, buf = cv2.imencode('.png', raw_image)
            # raw_image = raw_image.copy(order='C')
            status['camera_rgb']['image'] = 'data:image/png;base64,' + base64.b64encode(buf).decode("utf-8")
            status['camera_rgb']['type'] = 'base64'

        # status['camera_rgb']['image'] = None
        return status
