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
