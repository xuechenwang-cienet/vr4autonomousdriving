#!/bin/env python2

import carla
import time
import json

from vrserver.util import BaseActor
from vrserver.util import PlayerNotFoundError
from vrserver.sensormanager import SensorManager
from vrserver.sensorlistener import SensorListener


class Venv(BaseActor):
    def __init__(self, ip, port):
        super(Venv, self).__init__()
        self._client = carla.Client(ip, port)
        self._client.set_timeout(2.0)

        self._player = None
        self._sensor_manager = SensorManager()

        actors = self._client.get_world().get_actors()
        while len(actors) == 0:
            time.sleep(2.0)
            actors = self._client.get_world().get_actors()
        for actor in actors:
            print(actor)
            if actor.type_id.startswith('vehicle.') or actor.type_id.startswith('sensor.'):
                actor.destroy()

    def set_player(
            self,
            vehicle_name='vehicle.lincoln.mkz2017',
            role_name='hero',
            color_id=0,
            position_id=0,
            autopilot=False):

        actors = self._client.get_world().get_actors()
        for actor in actors:
            print(actor)
            if actor.type_id==vehicle_name:
                actor.set_simulate_physics(False)
                actor.set_transform(self._client.get_world().get_map().get_spawn_points()[position_id])
                actor.set_simulate_physics(True)
                return

        blueprint = self._client.get_world().get_blueprint_library().find(vehicle_name)
        print('recommended_values:', len(blueprint.get_attribute('color').recommended_values))
        blueprint.set_attribute('role_name', 'hero')
        blueprint.set_attribute('color', blueprint.get_attribute('color').recommended_values[color_id])
        print('get_spawn_points:', len((self._client.get_world().get_map().get_spawn_points())))
        self._player = self._client.get_world().try_spawn_actor(blueprint, self._client.get_world().get_map().get_spawn_points()[position_id])
        print('created %s' % self._player.type_id)

        autopilot = True
        self._player.set_autopilot(autopilot)
        self._sensor_manager.add_parent_actor(self._player)

    def set_vehicle(
            self,
            vehicle_name='vehicle.audi.tt',
            role_name='hero',
            color_id=0,
            position_id=0):


        blueprint = self._client.get_world().get_blueprint_library().find(vehicle_name)
        print('recommended_values:', len(blueprint.get_attribute('color').recommended_values))
        blueprint.set_attribute('role_name', 'hero')
        blueprint.set_attribute('color', blueprint.get_attribute('color').recommended_values[color_id])
        print('get_spawn_points:', len((self._client.get_world().get_map().get_spawn_points())))

        transform = self._client.get_world().get_map().get_spawn_points()[position_id]
        

        self._client.get_world().try_spawn_actor(blueprint, waypoint.next(20.0).transform)

    def add_listener(self, listener):
        if self._sensor_manager is None:
            raise PlayerNotFoundError('No SensorManager Found')
        self._sensor_manager.add_listener(listener)

    def get_player_status(self):
        if self._player is None:
            raise PlayerNotFoundError('No Player Found')
        if self._sensor_manager is None:
            raise PlayerNotFoundError('No SensorManager Found')
        return json.dumps(self._sensor_manager.get_status(True))
