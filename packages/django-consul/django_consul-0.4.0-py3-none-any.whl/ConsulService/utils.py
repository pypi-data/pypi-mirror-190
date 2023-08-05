import requests
from .settings import *


_service_payload = {
    "ID": SERVICE_ID,
    "Name": SERVICE_NAME,
    "Tags": ["primary", "v1"],
    "Address": SERVICE_ADDRESS,
    "Port": SERVICE_PORT,
    "Meta": {
        "version": SERVICE_VERSION
    },
    "EnableTagOverride": True,
    "Check": {
        "http": CHECK_URL,
        "Interval": "10s",
        "Timeout": "5s"
    },
    "Weights": {
        "Passing": 10,
        "Warning": 1
    }
}


def do_register():
    service_url = f"{AGENT_SCHEME}://{AGENT_ADDRESS}:{AGENT_PORT}/v1/agent/service/register"
    rsp = requests.put(service_url, json=_service_payload)
    print(rsp.status_code, rsp.text)

    kv_url = f"{AGENT_SCHEME}://{AGENT_ADDRESS}:{AGENT_PORT}/v1/kv/upstreams/{SERVICE_NAME}/{SERVICE_ADDRESS}:{SERVICE_PORT}"
    rsp = requests.put(url=kv_url, json={
      "weight": 1,
      "max_fails": 2,
      "fail_timeout": 10,
      "down": 0
    })
    print(rsp.status_code, rsp.text)
