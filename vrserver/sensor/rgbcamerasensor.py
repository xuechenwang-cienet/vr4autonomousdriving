#!/bin/env python3

import numpy as np
import weakref
import datetime

import carla


class RGBCameraSensor(object):
    def __init__(self, parent_actor):
        self.sensor = None
        self._parent = parent_actor

        self.camera_rgb = None
        self.timestamp = None

        world = self._parent.get_world()
        bp = world.get_blueprint_library().find('sensor.camera.rgb')
        bp.set_attribute('image_size_x', str(800))
        bp.set_attribute('image_size_y', str(600))
        self.sensor = world.spawn_actor(bp, carla.Transform(carla.Location(x=1.6, z=1.7), carla.Rotation(pitch=-15)), attach_to=self._parent)
        # We need to pass the lambda a weak reference to self to avoid circular
        # reference.
        weak_self = weakref.ref(self)
        self.sensor.listen(lambda event: RGBCameraSensor._on_camera_rgb_event(weak_self, event))

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

        self.camera_rgb = array
        self.timestamp = datetime.datetime.now()

    def destroy(self):
        if self.sensor is not None:
            self.sensor.destroy()