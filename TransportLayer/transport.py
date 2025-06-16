import threading
import random
from TransportLayer.sliding_window import go_back_n_send, go_back_n_receive

class TransportLayer:
    def __init__(self):
        self.port_table = {}  # port_no: process_name
        self.lock = threading.Lock()
        self.next_ephemeral = 1024

    def assign_port(self, process_name, port_no=None):
        with self.lock:
            if port_no is None:
                # Assign ephemeral port
                while self.next_ephemeral in self.port_table:
                    self.next_ephemeral += 1
                port = self.next_ephemeral
                self.port_table[port] = process_name
                return port
            else:
                self.port_table[port_no] = process_name
                return port_no

    def send(self, src_port, dst_port, data, channel):
        # Use Go-Back-N for reliable delivery
        print(f"[Transport] Sending from port {src_port} to port {dst_port}: {data}")
        go_back_n_send(data, channel, src_port, dst_port)

    def receive(self, port, channel):
        # Use Go-Back-N for reliable delivery
        data = go_back_n_receive(channel, port)
        print(f"[Transport] Received at port {port}: {data}")
        return data