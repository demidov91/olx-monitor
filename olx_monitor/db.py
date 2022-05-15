import os

import motor

from contextvars import ContextVar


_connections = {}
_connection = ContextVar('connection')


def get_connection():
    return motor.MotorClient(os.environ['DB_CONNSTRING'])


def update_active_connection():
    _connection.set(get_connection())


def subscription() -> 'motor.core.AgnosticDatabase':
    return _connection.get()['olx-monitor']['subscription']

