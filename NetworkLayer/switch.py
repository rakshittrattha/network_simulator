class Switch:
    def __init__(self, name):
        self.name = name
        self.ports = {}
        self.mac_table = {}

    def connect_device(self, device, port):
        self.ports[port] = device
        print(f"[{self.name}] connected {device.name if hasattr(device, 'name') else 'Router'} at port {port}")

    def receive_frame(self, frame, sender):
        sender_port = self.find_port(sender) #Gets the port number on which the sender is connected .



        if 'sender_mac' in frame:
            self.mac_table[frame['sender_mac']] = sender_port
        elif 'l2' in frame:
            self.mac_table[frame['l2']['src_mac']] = sender_port

        self.print_mac_table()

        if frame['type'] == 'ARP_REQUEST':
            for port, device in self.ports.items():
                if device != sender:#Floods the ARP request to all other devices except the sender.


                    print(f"[{self.name}] flooding ARP Request to {getattr(device, 'name', 'Router')}")
                    device.receive_arp_request(frame)

        elif frame['type'] == 'ARP_REPLY':
            dst_mac = frame['target_mac']
            if dst_mac in self.mac_table:
                out_port = self.mac_table[dst_mac]
                dest_device = self.ports[out_port]
                print(f"[{self.name}] unicasting ARP Reply to {getattr(dest_device, 'name', 'Router')}")
                dest_device.receive_arp_reply(frame)

        elif frame['type'] == 'DATA': #For regular data frames (e.g., after ARP is done and MAC is known):

            dst_mac = frame['l2']['dst_mac']
            if dst_mac in self.mac_table:
                out_port = self.mac_table[dst_mac]
                dest_device = self.ports[out_port]
                print(f"[{self.name}] forwarding DATA frame to {getattr(dest_device, 'name', 'Router')}")
                dest_device.receive_data(frame)
            else:
                print(f"[{self.name}] unknown destination MAC {dst_mac}, flooding not implemented for DATA")

    def find_port(self, device):
        for port, dev in self.ports.items():
            if dev == device:
                return port
        return None

    def print_mac_table(self):
        print(f"[{self.name}] MAC Table: {self.mac_table}")