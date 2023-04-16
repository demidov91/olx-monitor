import os

import motor.motor_asyncio

from contextvars import ContextVar


_connections = {}
_connection = ContextVar('connection')


def get_connection():
    return motor.motor_asyncio.AsyncIOMotorClient(os.environ['DB_CONNSTRING'])


def update_active_connection():
    _connection.set(get_connection())


def subscription_collection() -> 'motor.core.AgnosticDatabase':
    return _connection.get()[os.environ['DATABASE_NAME']]['subscription']

