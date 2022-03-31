# pods_store.py


class PodStore:
    def __init__(self):
        self.pods = {}  # pod_id -> {cpu_required, assigned_node}

    def add_pod(self, pod_id, cpu_required, assigned_node):
        self.pods[pod_id] = {
            "cpu_required": cpu_required,
            "assigned_node": assigned_node,
        }
