from django.conf import settings


def get(key, default):
    return getattr(settings, key, default)


AGENT_SCHEME = get('CONSUL_AGENT_SCHEME', 'http')
AGENT_ADDRESS = get('CONSUL_AGENT_ADDRESS', "consul.local")
AGENT_PORT = get('CONSUL_AGENT_PORT', 8500)
CHECK_URL = get('CONSUL_CHECK_URL', 'http://127.0.0.1:8000/healthy')
CHECK_INTERVAL = get('CONSUL_CHECK_INTERVAL', '10s')

SERVICE_NAME = get('CONSUL_SERVICE_NAME', 'unknown-service')
SERVICE_ID = get('CONSUL_SERVICE_ID', SERVICE_NAME)
SERVICE_ADDRESS = get('CONSUL_SERVICE_ADDRESS', '127.0.0.1')
SERVICE_PORT = get('CONSUL_SERVICE_PORT', 8000)
SERVICE_VERSION = get('CONSUL_SERVICE_VERSION', '0.0.0')



