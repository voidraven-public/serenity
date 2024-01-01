import subprocess

def run_ansible_playbook(playbook_path):
    try:
        subprocess.run(['ansible-playbook', playbook_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run playbook: {e}")
    else:
        print("Playbook executed successfully")

# Replace 'your_playbook.yml' with the path to your Ansible playbook
run_ansible_playbook('your_playbook.yml')



# ###### 
import subprocess
import shlex

def execute_ansible_playbook(playbook_path, extra_vars=None):
    """Executes an Ansible playbook with optional extra variables.

    Args:
        playbook_path (str): Path to the Ansible playbook file.
        extra_vars (dict, optional): Dictionary of extra variables to pass to the playbook.
            Defaults to None.

    Returns:
        tuple: A tuple containing the playbook's return code and output.
    """

    command = f"ansible-playbook {playbook_path}"

    if extra_vars:
        extra_vars_str = shlex.quote(json.dumps(extra_vars))  # Safely quote extra_vars
        command += f" -e {extra_vars_str}"

    try:
        process = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error executing playbook: {e}")
        return e.returncode, e.output

    return process.returncode, process.stdout

# Example usage:
playbook_path = "/path/to/your/playbook.yml"
extra_vars = {"variable1": "value1", "variable2": "value2"}  # Optional

return_code, output = execute_ansible_playbook(playbook_path, extra_vars)

if return_code == 0:
    print("Playbook execution successful!")
else:
    print("Playbook execution failed with return code:", return_code)
    print("Output:\n", output)
