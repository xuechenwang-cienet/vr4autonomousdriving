#!/bin/env python3

import time
import json
import uuid

import carla

from vrserver.util import BaseActor


class Venv(BaseActor):
    def __init__(self, ip, port):
        super(Venv, self).__init__()
        self._client = carla.Client(ip, port)
        self._client.set_timeout(2.0)

        self._npc_actors = {}

        self._pure_venv_all()

    def __del__(self):
        self._pure_venv_all()

    def _pure_venv_all(self):
        actors = self._client.get_world().get_actors()
        while len(actors) == 0:
            time.sleep(2.0)
            actors = self._client.get_world().get_actors()
        for actor in actors:
            print(actor)
            if actor.type_id.startswith('vehicle.') or actor.type_id.startswith('sensor.'):
                actor.destroy()

    def _build_vehicle_blueprint(
            self,
            vehicle_type='vehicle.lincoln.mkz2017',
            role_name='hero',
            color_id=0):
        blueprint = self._client.get_world().get_blueprint_library().find(vehicle_type)
        blueprint.set_attribute('role_name', role_name)
        blueprint.set_attribute(
            'color', blueprint.get_attribute('color').recommended_values[color_id])
        return blueprint

    def _spawn_actor(self, vehicle_name, blueprint, transform):
        actor = self._client.get_world().try_spawn_actor(blueprint, transform)
        self._npc_actors[vehicle_name] = actor
        print('created %s' % actor.type_id)
        return actor

    def acquire_vehicle_with_position_id(
            self,
            vehicle_name,
            vehicle_type='vehicle.lincoln.mkz2017',
            role_name='hero',
            color_id=0,
            position_id=10):

        blueprint = self._build_vehicle_blueprint(vehicle_type, role_name, color_id)
        transform = self._client.get_world().get_map().get_spawn_points()[position_id]

        actor = self._spawn_actor(vehicle_name, blueprint, transform)

        return actor

    def acquire_vehicle_with_location(
            self,
            vehicle_name=str(uuid.uuid4()),
            vehicle_type='vehicle.audi.tt',
            role_name='hero',
            color_id=0,
            location_x=71.6,
            location_y=-195.7,
            rotation_yaw=1.43954):

        blueprint = self._build_vehicle_blueprint(vehicle_type, role_name, color_id)

        transform = self._client.get_world().get_map().get_spawn_points()[0]
        transform.location.x = location_x
        transform.location.y = location_y
        transform.rotation.yaw = rotation_yaw

        actor = self._spawn_actor(vehicle_name, blueprint, transform)

        return actor
