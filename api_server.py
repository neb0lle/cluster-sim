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
