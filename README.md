# Distributed Cluster Simulation

A Python-based distributed cluster simulation that demonstrates container orchestration concepts similar to Kubernetes, but on a smaller scale. The system allows you to create nodes, schedule pods, and handles automatic health checks and pod rescheduling.

## Features

- Node registration and health monitoring
- Pod scheduling with CPU resource management
- Automatic pod rescheduling on node failure
- Real-time node health checks via heartbeat mechanism
- Web-based dashboard for cluster visualization
- RESTful API for cluster management

## Architecture

The system consists of the following components:

- **API Server**: Central management component that handles node registration, pod scheduling, and health monitoring
- **Node Containers**: Docker containers that simulate cluster nodes
- **Node Store**: Manages node state and scheduling logic
- **Pod Store**: Handles pod metadata and assignment

## Screenshots

### Dashboard View
[Insert dashboard screenshot here showing the cluster overview]

### Node Health Status
[Insert screenshot showing node health monitoring]

### Pod Distribution
[Insert screenshot showing pod distribution across nodes]

## Setup Instructions

1. Ensure you have Python 3.9+ and Docker installed on your system

2. Clone the repository:
bash
git clone [your-repository-url]
cd [repository-name]


3. Install the required Python packages:
bash
pip install flask requests


4. Build the node container image:
bash
docker build -t cluster-node -f Dockerfile.node .


5. Start the API server:
bash
python api_server.py


## API Endpoints

### Register Node
- **Endpoint**: `/register_node`
- **Method**: POST
- **Body**:
json
{
    "node_id": "node-1",
    "cpu_cores": 4
}


### Launch Pod
- **Endpoint**: `/launch_pod`
- **Method**: POST
- **Body**:
json
{
    "pod_id": "pod-1",
    "cpu_required": 2