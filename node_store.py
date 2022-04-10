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

    def update_heartbeat(self, node_id):
        if node_id in self.nodes:
            self.last_heartbeat[node_id] = time.time()
            self.nodes[node_id]["status"] = "healthy"

    def check_node_health(self, pod_store, timeout=10):
        now = time.time()
        for node_id in list(self.nodes.keys()):
            last_seen = self.last_heartbeat.get(node_id)
            if last_seen and (now - last_seen > timeout):
                if self.nodes[node_id]["status"] == "healthy":
                    print(f"[!] Node {node_id} marked as unhealthy.")
                    self.nodes[node_id]["status"] = "unhealthy"
                    self.reschedule_pods(node_id, pod_store)
