#!/bin/env python2

from vrserver.util import BaseActor


class Controller(BaseActor):
    def __init__(self, venv, ctu):
        super(Controller, self).__init__()
