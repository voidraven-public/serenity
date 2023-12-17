import subprocess

node_name = "my-node"
grace_period = 300  # Adjust as needed

command = f"kubectl drain node {node_name} --grace-period={grace_period}"
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
output, error = process.communicate()


if process.returncode != 0:
    print(f"Error draining node: {error.decode()}")
else:
    print(f"Node '{node_name}' successfully drained.")