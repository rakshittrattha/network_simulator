def telnet_server(transport, listen_port, channel):
    print(f"[Telnet Server] Listening on port {listen_port}")
    command = transport.receive(listen_port, channel)
    print(f"[Telnet Server] Command received: {command}")
    # Simulate command execution (for demo, just echo a canned response)
    if command == "date":
        response = "Thu Jun  4 12:34:56 2025"
    elif command == "whoami":
        response = "student"
    else:
        response = f"Unknown command: {command}"
    transport.send(listen_port, listen_port+1, response, channel)

def telnet_client(transport, server_port, command, channel):
    src_port = transport.assign_port("telnet_client")
    print(f"[Telnet Client] Sending command '{command}' to port {server_port}")
    transport.send(src_port, server_port, command, channel)
    reply = transport.receive(src_port, channel)
    print(f"[Telnet Client] Received response: {reply}")