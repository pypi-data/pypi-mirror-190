# django-consul
 
 A Django app which registering service to consul agent at start time.
 
## Installation

```shell script
pip install django-consul
```

## Configurations

Add `ConsulService` to INSTALLED_APPS setting.

CONSUL_AGENT_ADDRESS Consul agent server's address

CONSUL_AGENT_PORT Consul agent server's port

CONSUL_CHECK_URL API on service used by consul server to check it's status

CONSUL_CHECK_INTERVAL Status check interval

CONSUL_SERVICE_NAME Local service name

CONSUL_SERVICE_ADDRESS Local service address

SERVICE_PORT Local service port
