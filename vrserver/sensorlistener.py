#!/bin/env python2

from vrserver.util import BaseActor


class SensorListener(BaseActor):  

    def on_gnss_event(self, gnss_event):
        pass

    def on_camera_rgb_event(self, image):
        pass
