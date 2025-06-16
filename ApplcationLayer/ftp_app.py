def ftp_server(transport, listen_port, channel, files):
    print(f"[FTP Server] Listening on port {listen_port}")
    filename = transport.receive(listen_port, channel)
    print(f"[FTP Server] File requested: {filename}")
    content = files.get(filename, "File not found")
    transport.send(listen_port, listen_port+1, content, channel)

def ftp_client(transport, server_port, filename, channel):
    src_port = transport.assign_port("ftp_client")
    print(f"[FTP Client] Requesting file '{filename}' from port {server_port}")
    transport.send(src_port, server_port, filename, channel)
    content = transport.receive(src_port, channel)
    print(f"[FTP Client] Received file content: {content}")