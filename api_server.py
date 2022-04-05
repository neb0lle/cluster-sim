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
