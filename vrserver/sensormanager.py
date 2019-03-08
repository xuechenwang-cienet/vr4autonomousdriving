#!/bin/env python2

import weakref
import numpy as np
import base64
import cv2

import carla

class SensorManager(object):
    def __init__(self):
        self._parent = None

        self._gnss_sensor = None
        self._camera_rgb_sensor = None
        self._lidar_sensor = None

        self._status = {}
        self._status['gnss'] = {
            'latitude': None,
            'longitude': None,
            'altitude': None}
        self._status['camera_rgb'] = {'image': None, 'type': 'raw'}
        self._status['lidar'] = {'data': None}

        self._listeners = []

    def destroy(self):
        for actor in [self._gnss_sensor, self._camera_rgb_sensor, self._lidar_sensor]:
            if actor is not None:
                actor.destroy()
    
    def __del__(self):
        self.destroy()

    def add_parent_actor(self, parent_actor):
        self._parent = parent_actor
        self._add_gnss()
        self._add_camera_rgb()
        self._add_lidar()

    def _add_gnss(self):
        world = self._parent.get_world()
        bp = world.get_blueprint_library().find('sensor.other.gnss')
        self.sensor = world.spawn_actor(bp, carla.Transform(carla.Location(x=1.0, z=2.8)), attach_to=self._parent)
        # We need to pass the lambda a weak reference to self to avoid circular
        # reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(lambda event: SensorManager._on_gnss_event(weak_self, event))

    @staticmethod
    def _on_gnss_event(weak_self, event):
        self = weak_self()
        if not self:
            return
        self._status['gnss']['latitude'] = event.latitude
        self._status['gnss']['longitude'] = event.longitude
        self._status['gnss']['altitude'] = event.altitude

        for listener in self._listeners:
            listener.on_gnss_event(self._status['gnss'])

    def _add_camera_rgb(self):
        world = self._parent.get_world()
        bp = world.get_blueprint_library().find('sensor.camera.rgb')
        bp.set_attribute('image_size_x', str(800))
        bp.set_attribute('image_size_y', str(600))
        self.sensor = world.spawn_actor(bp, carla.Transform(carla.Location(x=-5.5, z=2.8), carla.Rotation(pitch=-15)), attach_to=self._parent)
        # We need to pass the lambda a weak reference to self to avoid circular
        # reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(lambda event: SensorManager._on_camera_rgb_event(weak_self, event))

    @staticmethod
    def _on_camera_rgb_event(weak_self, image):
        self = weak_self()
        if not self:
            return
        image.convert(carla.ColorConverter.Raw)
        array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
        array = np.reshape(array, (image.height, image.width, 4))
        array = array[:, :, :3]
        # self._surface = pygame.surfarray.make_surface(array.swapaxes(0, 1))

        self._status['camera_rgb']['image'] = array

        for listener in self._listeners:
            listener.on_camera_rgb_event(self._status['camera_rgb'])

    def _add_lidar(self):
        pass

    def add_listener(self, listener):
        if listener not in self._listeners:
            self._listeners.append(listener)

    def get_status(self, convert=False):
        if convert and self._status['camera_rgb']['image'] is not None:
            status = self._status.copy()
            raw_image = status['camera_rgb']['image']
            _, buf = cv2.imencode('.png', raw_image)
            # raw_image = raw_image.copy(order='C')
            status['camera_rgb']['image'] = 'data:image/png;base64,' + base64.b64encode(buf)
            status['camera_rgb']['type'] = 'base64'
            return status
        return self._status
