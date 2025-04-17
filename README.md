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
}


### List Nodes
- **Endpoint**: `/list_nodes`
- **Method**: GET

### Node Heartbeat
- **Endpoint**: `/heartbeat`
- **Method**: POST
- **Body**:
json
{
    "node_id": "node-1"
}


### Dashboard
- **Endpoint**: `/dashboard`
- **Method**: GET

## System Behavior

### Node Health Monitoring
- Nodes send heartbeats every 5 seconds
- Nodes are marked unhealthy after 10 seconds of no heartbeat
- Pods are automatically rescheduled from unhealthy nodes

### Pod Scheduling
- Uses a First-Fit scheduling strategy
- Considers available CPU resources on nodes
- Ensures pods are only scheduled on healthy nodes

## Error Handling

The system handles various error scenarios:
- Node failures
- Resource exhaustion
- Duplicate node/pod registration
- Invalid requests

## System Testing

### Prerequisites
- Python 3.9+
- Docker
- curl or Postman for API testing
- pytest (for automated tests)

### Manual Testing

1. **Start the API Server**
bash
python api_server.py


2. **Register Nodes**
bash
# Register first node
curl -X POST http://localhost:5000/register_node \
  -H "Content-Type: application/json" \
  -d '{"node_id": "node-1", "cpu_cores": 4}'

# Register second node
curl -X POST http://localhost:5000/register_node \
  -H "Content-Type: application/json" \
  -d '{"node_id": "node-2", "cpu_cores": 2}'


3. **Verify Node Registration**
bash
curl http://localhost:5000/list_nodes


4. **Launch Pods**
bash
# Launch first pod
curl -X POST http://localhost:5000/launch_pod \
  -H "Content-Type: application/json" \
  -d '{"pod_id": "pod-1", "cpu_required": 2}'

# Launch second pod
curl -X POST http://localhost:5000/launch_pod \
  -H "Content-Type: application/json" \
  -d '{"pod_id": "pod-2", "cpu_required": 1}'


5. **Test Node Failure**
bash
# Stop a node container to simulate failure
docker stop node-1

# Wait for 10 seconds (heartbeat timeout)
# Check pod rescheduling
curl http://localhost:5000/list_nodes


6. **View Dashboard**
Open `http://localhost:5000/dashboard` in your browser to view the cluster state.

### Automated Testing

1. **Install Test Dependencies**
bash
pip install pytest pytest-cov


2. **Run Tests**
bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=.


### Test Scenarios

1. **Node Registration Tests**
   - Register valid node
   - Register duplicate node
   - Register node with invalid CPU cores

2. **Pod Scheduling Tests**
   - Schedule pod on available node
   - Schedule pod when no nodes available
   - Schedule pod with invalid CPU requirements

3. **Health Monitoring Tests**
   - Verify heartbeat updates
   - Test node failure detection
   - Verify pod rescheduling

4. **Resource Management Tests**
   - Test CPU allocation
   - Test resource exhaustion
   - Test resource release

### Testing Best Practices

1. **Isolation**
   - Use separate Docker networks for testing
   - Clean up test containers after each test
   - Use unique node IDs for each test

2. **Monitoring**
   - Check system logs during testing
   - Monitor resource usage
   - Verify expected state transitions

3. **Edge Cases**
   - Test with maximum number of nodes
   - Test with maximum CPU allocation
   - Test rapid node failures

### Performance Testing

1. **Load Testing**
bash
# Example using Apache Benchmark
ab -n 1000 -c 10 http://localhost:5000/list_nodes


2. **Resource Monitoring**
bash
# Monitor Docker containers
docker stats

# Monitor system resources
top


3. **Stress Testing**
   - Create multiple nodes simultaneously
   - Schedule multiple pods rapidly
   - Simulate multiple node failures