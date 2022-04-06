# api_server.py

import subprocess
import uuid
from flask import Flask, request, jsonify
from node_store import NodeStore
from pods_store import PodStore

app = Flask(__name__)

store = NodeStore()
pod_store = PodStore()


@app.route("/")
def home():
    return "Distributed Cluster Simulation API Running"


# Launch a new Docker container simulating a node
def launch_node_container(node_id, cpu_cores):
    try:
        subprocess.run(
            [
                "docker",
                "run",
                "-d",
                "--name",
                node_id,
                "-e",
                f"NODE_ID={node_id}",
                "-e",
                f"CPU_CORES={cpu_cores}",
                "-e",
                "API_SERVER=http://host.docker.internal:5000",
                "cluster-node",
            ],
            check=True,
        )
        print(f"[+] Launched container for node {node_id}")
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to launch container: {e}")


# Register a node and launch its container
@app.route("/register_node", methods=["POST"])
def register_node():
    data = request.get_json()
    node_id = data.get("node_id")
    cpu_cores = data.get("cpu_cores")

    if not node_id or cpu_cores is None:
        return jsonify({"error": "Missing node_id or cpu_cores"}), 400

    success = store.register_node(node_id, cpu_cores)
    if success:
        launch_node_container(node_id, cpu_cores)
        return jsonify(
            {"message": f"Node '{node_id}' registered and container launched."}
        ), 200
    else:
        return jsonify({"message": f"Node '{node_id}' already exists."}), 409


# View all nodes (with auto health check + rescheduling)
@app.route("/list_nodes", methods=["GET"])
def list_nodes():
    return jsonify(store.get_all_nodes(pod_store))


# Heartbeat from node containers
@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    data = request.get_json()
    node_id = data.get("node_id")

    if not node_id:
        return jsonify({"error": "Missing node_id"}), 400

    store.update_heartbeat(node_id)
    return jsonify({"message": f"Heartbeat received from '{node_id}'"}), 200


# Launch a new pod, assign to healthy node
@app.route("/launch_pod", methods=["POST"])
def launch_pod():
    data = request.get_json()
    pod_id = data.get("pod_id")
    cpu_required = data.get("cpu_required")

    if not pod_id or cpu_required is None:
        return jsonify({"error": "Missing pod_id or cpu_required"}), 400

    if pod_store.pod_exists(pod_id):
        return jsonify({"error": f"Pod '{pod_id}' already exists"}), 409

    result = store.schedule_pod(pod_id, cpu_required)
    if result:
        pod_store.add_pod(pod_id, cpu_required, result["assigned_node"])
        return jsonify(
            {
                "message": f"Pod '{pod_id}' scheduled on node '{result['assigned_node']}'",
                "node_id": result["assigned_node"],
            }
        ), 200
    else:
        return jsonify({"error": "No healthy node has enough CPU"}), 503


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
