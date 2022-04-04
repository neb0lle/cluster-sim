# pods_store.py


class PodStore:
    def __init__(self):
        self.pods = {}  # pod_id -> {cpu_required, assigned_node}

    def add_pod(self, pod_id, cpu_required, assigned_node):
        self.pods[pod_id] = {
            "cpu_required": cpu_required,
            "assigned_node": assigned_node,
        }

    def pod_exists(self, pod_id):
        return pod_id in self.pods

    def get_all_pods(self):
        return self.pods

    def remove_pod(self, pod_id):
        if pod_id in self.pods:
            del self.pods[pod_id]
