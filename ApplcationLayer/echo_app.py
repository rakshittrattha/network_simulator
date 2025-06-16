def echo_server(transport, listen_port, channel):
    print(f"[Echo Server] Listening on port {listen_port}")
    data = transport.receive(listen_port, channel)
    print(f"[Echo Server] Received: {data}")
    transport.send(listen_port, listen_port+1, data, channel)

def echo_client(transport, server_port, message, channel):
    src_port = transport.assign_port("echo_client")
    print(f"[Echo Client] Sending '{message}' to port {server_port}")
    transport.send(src_port, server_port, message, channel)
    reply = transport.receive(src_port, channel)
    print(f"[Echo Client] Received echo: {reply}")
