# node.py

import os
import time
import requests

node_id = os.getenv("NODE_ID", "unnamed-node")
cpu_cores = int(os.getenv("CPU_CORES", 2))
api_url = os.getenv("API_SERVER", "http://host.docker.internal:5000")


def register():
    print(f"[{node_id}] Registering with API server...")
    try:
        res = requests.post(
            f"{api_url}/register_node",
            json={"node_id": node_id, "cpu_cores": cpu_cores},
        )
        print(res.text)
    except Exception as e:
        print(f"Registration failed: {e}")


def send_heartbeat():
    try:
        res = requests.post(f"{api_url}/heartbeat", json={"node_id": node_id})
        print(f"[{node_id}] Heartbeat sent.")
    except Exception as e:
        print(f"[{node_id}] Heartbeat failed: {e}")


if __name__ == "__main__":
    register()
    while True:
        send_heartbeat()
        time.sleep(5)
