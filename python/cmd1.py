import subprocess

command = "ls -l"  # Replace with your desired Bash command

result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

if result.returncode == 0:
    output = result.stdout
    for line in result.stdout.splitlines():
        print(line.decode('utf-8'))
else:
    error = result.stderr
    print("Command error:", error)