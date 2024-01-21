import subprocess

# Define the Kubernetes pod name, namespace, and the command to run
pod_name = "your-pod-name"
namespace = "your-namespace"
command_to_run = ["sh", "-c", "your-shell-command"]

# Construct the kubectl command to execute the command in the pod
kubectl_command = f"ls"

try:
    # Execute the kubectl command and capture the output
    output = subprocess.check_output(kubectl_command, shell=True, text=True)
    
    # Print the output
    print("Command Output:")
    print(output)
except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e}")
