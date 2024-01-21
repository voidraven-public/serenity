import subprocess

# The shell command you want to execute
command = "your-shell-command"

try:
    # Execute the command and capture its output
    result = subprocess.check_output(command, shell=True, text=True)
    
    # Print or process the captured output
    print("Command Output:")
    print(result)
except subprocess.CalledProcessError as e:
    print(f"Error executing command: {e}")
