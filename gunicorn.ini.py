import os
from copy import copy
from multiprocessing import cpu_count

CPU_COUNT = cpu_count()


#
# Determines configuration for Gunicorn server:
#   1 - determines defaults based on environment
#   2 - grabs config from environment, using defaults


def get_env_specific_defaults(defaults):
    """
    Update configuration defaults if development
    :param defaults: {}
    :return: {}
    """
    new_defaults = copy(defaults)
    IS_DEV = os.getenv('ENV') == 'development'

    # overwrite defaults
    new_defaults['LOG_LEVEL'] = 'debug' if IS_DEV else defaults['LOG_LEVEL']
    new_defaults['MAX_REQUESTS'] = 1 if IS_DEV else defaults['MAX_REQUESTS']

    return new_defaults


# 1
DEFAULTS = get_env_specific_defaults({
    'MAX_REQUESTS': 0,  # default to no restarts, handle inf requests
    'BIND_ADDRESS': '0.0.0.0',  # bind to local
    'SOCKET': 'unix:/run/gunicorn/socket',
    'PORT': '8000',
    'WORKERS': 2 * CPU_COUNT + 1,  # default worker count to utilize processors
    'LOG_LEVEL': 'error'
})


def get_env_or_default(var_name):
    """
    Retrieve from env or resort to defaults
    :param var_name: string
    :return: config var value
    """
    expected_env_var = '_'.join(['GUNICORN', var_name])
    return os.environ.get(expected_env_var, DEFAULTS[var_name])


def get_bound_address():
    """
    Build bound address for server
    :return: string
    """
    if 'GUNICORN_SOCKET' in os.environ:
        return get_env_or_default('SOCKET')

    return ":".join([
        get_env_or_default('BIND_ADDRESS'),
        get_env_or_default('PORT')
    ])


# 2
max_requests = get_env_or_default('MAX_REQUESTS')
bind = get_bound_address()
workers = get_env_or_default('WORKERS')
loglevel = get_env_or_default('LOG_LEVEL')
