# node_store.py

import time


class NodeStore:
    def __init__(self):
        self.nodes = {}
        self.last_heartbeat = {}

    def register_node(self, node_id, cpu_cores):
        if node_id in self.nodes:
            return False
        self.nodes[node_id] = {
            "cpu_cores": cpu_cores,
            "available_cpu": cpu_cores,
            "pods": [],
            "status": "healthy",
        }
        self.last_heartbeat[node_id] = time.time()
        return True
