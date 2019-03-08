#!/bin/env python2

import pykka


class BaseActor(pykka.ThreadingActor):
    def ping(self):
        return True


class APPError(Exception):
    def __init__(self, message):
        super(APPError, self).__init__()
        self.message = '{"error":"%s"}' % message


class PlayerNotFoundError(APPError):
    def __init__(self, message):
        super(PlayerNotFoundError, self).__init__(message)
