import subprocess

command = "ls -l"  # Replace with your desired Bash command

result = subprocess.run(command, shell=True, capture_output=True, text=True)

if result.returncode == 0:
    output = result.stdout
    print("Command output:", output)
else:
    error = result.stderr
    print("Command error:", error)