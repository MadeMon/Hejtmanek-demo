import subprocess
import json
import argparse

# TODO - Make these configurable
DEPLOYMENT_NAME = "demo-application"

def install_helm_chart(helm_dir, values):
    flat_values = flatten_json(values)
    value_str = ','.join(f"{k}={v}" for k, v in flat_values.items())

    print(f"Installing helm chart with values: {value_str}")
    result = subprocess.run(["helm", "install", DEPLOYMENT_NAME, "--set", value_str, helm_dir], capture_output=True, text=True)
    return result

def run_yaks_test(feature_path, values, expected_result):
    flat_values = flatten_json(values)
    env_values_str = ' '.join(f"-e {k}={v}" for k, v in flat_values.items())

    print("Running YAKS test")
    result = subprocess.run(["yaks", "run", feature_path, env_values_str], capture_output=True, text=True)

    exit_code = result.returncode
    
    return expected_result == "success" and exit_code == 0 or expected_result == "failure" and exit_code != 0

def print_test_results(results):
    print(f"Passed: {results['passed']}")
    print(f"Failed: {results['failed']}")

def uninstall_helm_chart():
    result = subprocess.run(["helm", "uninstall", DEPLOYMENT_NAME], capture_output=True, text=True)

def load_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            return json.load(stream)
        except json.JSONDecodeError as exc:
            print(exc)

def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for a in x:
                flatten(x[a], name + a + '.')
        elif isinstance(x, list):
            i = 0
            for a in x:
                flatten(a, name + str(i) + '.')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a JSON config file.')
    parser.add_argument('config_file', type=str, help='Path to the JSON config file')

    args = parser.parse_args()

    config = load_config(args.config_file)

    results = {"failed": 0, "passed": 0}

    for combinations in config['values_combinations']:
        uninstall_helm_chart()
        install_helm_chart(config['helm_dir'], combinations['values'])
        test_result = run_yaks_test(config['feature_file'], combinations['values'], combinations['expected_result'])

        if test_result:
            results["passed"] += 1
        else:
            results["failed"] += 1

    print_test_results(results)