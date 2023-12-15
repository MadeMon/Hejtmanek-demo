# Kubernetes application testing demo 
This repository contains a demo application, its Helm chart, a feature file describing the application's expected behavior, and a test configuration file.

## Demo Application

The application can be built into a Docker image and run as a container. It provides a web server that listens for incoming HTTP requests and responds with a simple message.
It is located in the `demo-application` directory.

## Helm Chart

The Helm chart for deploying the demo application to a Kubernetes cluster is located in the `helm` directory. It includes configuration files for the service and the deployment.

## Feature File

The `test.feature` file contains steps that verify the application's expected functionality.

## Test Configuration

The `test-config.json` file is a configuration file for testing a Helm chart. It contains:
### Configuration structure
- `feature_file`: Path to the .feature file for testing the expected application behavior.
- `helm_dir`: Path to the directory containing the Helm chart for deployment of the tested application.
- `values_combinations`: An array of combinations of values, each with:
    - `values`: An object representing the values to be used in the Helm chart.
    - `expected_result`: The expected result of the test ("success" or "failure").

### Description of the `test-config.json` example
In the example, the first combination of values represents a valid configuration. Therefore, the test described by the `test.feature` file is expected to pass.

The second combination represents an invalid configuration. Consequently, the test is expected to fail.

## Running the Demo

### Use local cluster (Optional)
Requires **Docker**
1. Install Kind
```bash
brew install kind
```
2. Create cluster
```
kind create cluster
```

Source - [Kind installation documentation](https://kind.sigs.k8s.io/docs/user/quick-start#installation)

### Prerequisites

- existing Kubernetes cluster
- installed and configured kubectl

### Steps

1. Install YAKS CLI
    1. Download the CLI client https://github.com/citrusframework/yaks/releases/latest
    2. Extract the downloaded archive and copy the `yaks` executable to `/usr/bin/yaks`

2. Install the YAKS operator to the Kubernetes cluster
```bash
yaks install --global=false
```

3. Build the Docker image for the demo application:

```bash
docker build -t demo-application ./demo-application
```

4. Load the Docker image to the Kubernetes cluster

    #### For Kind
    ```bash
    kind load docker-image demo-application
    ```
    #### For Minikube
    ```bash
    minikube image load demo-application
    ```

4. Run the demo:

```bash
python3 ./main.py test-config.json
```

---
# Other notes
## Uninstall YAKS operator
```bash
yaks uninstall --all
```
## Stop and delete Kind cluster
```bash
kind delete cluster
```