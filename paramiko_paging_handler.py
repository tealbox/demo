import paramiko
import re
import time
import sys

def send_command_with_paging(
    ssh_client,
    command,
    prompt_regex=r"[#$>]\s*$",  # Default Cisco/Juniper prompt
    paging_patterns=None,
    timeout=30,
    chunk_size=1024
):
    """
    Execute command and handle paging prompts automatically.
    
    Args:
        ssh_client: paramiko SSHClient
        command: Command to run
        prompt_regex: Regex to detect end of output (device prompt)
        paging_patterns: List of regex patterns for paging prompts
        timeout: Total timeout in seconds
        chunk_size: Buffer size for reading
    
    Returns:
        Full command output as string
    """
    if paging_patterns is None:
        paging_patterns = [
            r"--More--",
            r"-- MORE --",
            r"Press any key to continue",
            r"\[Continue\]",
            r"q to quit"
        ]
    
    # Compile regexes
    prompt_re = re.compile(prompt_regex, re.MULTILINE)
    paging_res = [re.compile(p, re.IGNORECASE) for p in paging_patterns]
    
    # Open shell
    shell = ssh_client.invoke_shell()
    time.sleep(0.5)
    
    # Clear initial banner
    if shell.recv_ready():
        shell.recv(chunk_size)
    
    # Send command
    shell.send(command + "\n")
    
    output = ""
    start_time = time.time()
    
    while True:
        # Check timeout
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Command timed out after {timeout} seconds")
        
        # Wait for data
        time.sleep(0.2)
        
        if shell.recv_ready():
            chunk = shell.recv(chunk_size).decode('utf-8', errors='ignore')
            output += chunk
            
            # Check for paging prompt
            paging_found = False
            for pattern in paging_res:
                if pattern.search(chunk):
                    # Send space to continue (some devices need Enter)
                    shell.send(" ")
                    paging_found = True
                    break
            
            if not paging_found:
                # Check for end of output (prompt returned)
                if prompt_re.search(output):
                    # Wait a bit more to catch final lines
                    time.sleep(0.5)
                    while shell.recv_ready():
                        output += shell.recv(chunk_size).decode('utf-8', errors='ignore')
                    break
        
        # Optional: break if command completed without prompt
        if command.strip().lower() in ["exit", "quit"]:
            break
    
    # Clean up shell
    shell.close()
    return output

# Example usage
if __name__ == "__main__":
    # Device connection details
    device = {
        "hostname": "10.0.0.1",
        "username": "admin",
        "password": "cisco",
        "port": 22
    }
    
    try:
        # Connect via Paramiko
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(**device)
        
        print("Running 'show running-config' with paging handler...")
        output = send_command_with_paging(
            ssh,
            "show running-config",
            timeout=120  # Allow 2 minutes for large configs
        )
        
        # Save output
        with open("running_config.txt", "w") as f:
            f.write(output)
        print("✅ Output saved to running_config.txt")
        print(f"📊 Output length: {len(output)} characters")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    finally:
        ssh.close()