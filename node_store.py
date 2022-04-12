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

    def reschedule_pods(self, failed_node_id, pod_store):
        failed_pods = self.nodes[failed_node_id]["pods"]
        self.nodes[failed_node_id]["pods"] = []
        self.nodes[failed_node_id]["available_cpu"] = self.nodes[failed_node_id][
            "cpu_cores"
        ]

        for pod_id in failed_pods:
            cpu_required = pod_store.pods[pod_id]["cpu_required"]
            reassigned = False

            for node_id, info in self.nodes.items():
                if (
                    info["status"] == "healthy"
                    and info["available_cpu"] >= cpu_required
                ):
                    info["pods"].append(pod_id)
                    info["available_cpu"] -= cpu_required
                    pod_store.pods[pod_id]["assigned_node"] = node_id
                    print(f"[+] Pod {pod_id} rescheduled to {node_id}")
                    reassigned = True
                    break

            if not reassigned:
                print(f"[!] Pod {pod_id} could not be rescheduled.")

    def schedule_pod(self, pod_id, cpu_required):
        # Simple First-Fit strategy
        for node_id, info in self.nodes.items():
            if info["status"] == "healthy" and info["available_cpu"] >= cpu_required:
                info["pods"].append(pod_id)
                info["available_cpu"] -= cpu_required
                return {"assigned_node": node_id, "cpu_used": cpu_required}
        return None

    def get_all_nodes(self, pod_store):
        self.check_node_health(pod_store)  # ✅ pass pod_store to health check
        return self.nodes
