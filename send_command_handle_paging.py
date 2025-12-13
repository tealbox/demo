def send_command_handle_paging(conn, command, prompt="--More--"):
    output = ""
    conn.write_channel(command + "\n")
    
    while True:
        try:
            new_output = conn.read_channel()
            output += new_output
            
            if prompt in new_output:
                # Send space to continue
                conn.write_channel(" ")
            elif conn.find_prompt() in new_output:
                # Reached end (device prompt returned)
                break
        except Exception as e:
            break
    
    return output
