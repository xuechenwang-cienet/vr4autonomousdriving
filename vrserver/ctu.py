#!/bin/env python2

import pykka

from  vrserver.util import BaseActor


class CTU(BaseActor):
    def __init__(self):
        super(CTU, self).__init__()
