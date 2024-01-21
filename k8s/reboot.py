import paramiko

def reboot_remote_machine(hostname, username, password):
    # Create an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the server
        ssh.connect(hostname=hostname, username=username, password=password)
        
        # Execute the reboot command
        stdin, stdout, stderr = ssh.exec_command('sudo shutdown -r now')

        # Wait for the command to complete
        stdout.channel.recv_exit_status()

        print("Reboot command sent successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        ssh.close()

# Example usage
reboot_remote_machine('192.168.208.100', 'public1', '')
