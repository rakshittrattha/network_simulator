import ipaddress
#determines the network address from an IP and subnet mask.
def get_network(ip_str, prefix):
    return str(ipaddress.IPv4Network(f"{ip_str}/{prefix}", strict=False).network_address)
#Used for checking if two IPs are in the same network 

class Host:
    def __init__(self, name, ip, mac, gateway_ip):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.gateway_ip = gateway_ip
        self.arp_table = {}
        self.connected_port = None
        self.connected_switch = None
# Connects the host to a specific switch and port.
    def connect(self, switch, port):
        self.connected_port = port
        self.connected_switch = switch
        switch.connect_device(self, port)

    def send_data(self, dest_ip):
       print(f"\n[{self.name}] wants to send data to {dest_ip}")
       self.print_arp_table()
     
       my_network = get_network(self.ip, 24)
       dest_network = get_network(dest_ip, 24)
     
       if my_network == dest_network:
           if dest_ip not in self.arp_table:
               print(f"[{self.name}] doesn't know MAC of {dest_ip}, sending ARP Request")
               self.pending_packet = {'dst_ip': dest_ip, 'is_direct': True} #it remembers whom it wanted to send using self.pending_packet.
               self.send_arp_request(dest_ip)
               return
           dst_mac = self.arp_table[dest_ip]
       else:
           # Remote network
           if self.gateway_ip not in self.arp_table:
               print(f"[{self.name}] doesn't know MAC of gateway {self.gateway_ip}, sending ARP Request")
               self.pending_packet = {'dst_ip': dest_ip, 'is_direct': False}
               self.send_arp_request(self.gateway_ip)
               return
           dst_mac = self.arp_table[self.gateway_ip] #use known gateway MAC.
     
       # Yahan tak pohonchne ka matlab MAC mil chuka hai, directly send karo
       print(f"[{self.name}] prepares L2 header: src_mac={self.mac}, dst_mac={dst_mac}")
       print(f"[{self.name}] sends data to {dest_ip}")
       frame = {
           'type': 'DATA',
           'l2': {'src_mac': self.mac, 'dst_mac': dst_mac},
           'l3': {'src_ip': self.ip, 'dst_ip': dest_ip, 'payload': f"Hello from {self.name} to {dest_ip}"}
       }
       self.connected_switch.receive_frame(frame, self)


    def send_arp_request(self, target_ip):#to learn MAC address of target_ip
        frame = {
            'type': 'ARP_REQUEST',
            'sender_ip': self.ip,
            'sender_mac': self.mac,
            'target_ip': target_ip
        }
        self.connected_switch.receive_frame(frame, self)

    def receive_arp_reply(self, frame):
        print(f"[{self.name}] received ARP Reply: {frame['sender_ip']} is at {frame['sender_mac']}")
        self.arp_table[frame['sender_ip']] = frame['sender_mac']

        if hasattr(self, 'pending_packet'):
            dst_ip = self.pending_packet['dst_ip']
            is_direct = self.pending_packet.get('is_direct', False)
            needed_ip = dst_ip if is_direct else self.gateway_ip

            if needed_ip in self.arp_table:
                dst_mac = self.arp_table[needed_ip]
                print(f"[{self.name}] (after ARP) prepares L2 header: src_mac={self.mac}, dst_mac={dst_mac}")
                print(f"[{self.name}] (after ARP) sends data to {dst_ip}")
                frame = {
                    'type': 'DATA',
                    'l2': {'src_mac': self.mac, 'dst_mac': dst_mac},
                    'l3': {'src_ip': self.ip, 'dst_ip': dst_ip, 'payload': f"Hello from {self.name} to {dst_ip}"}
                }
                self.connected_switch.receive_frame(frame, self)
                del self.pending_packet

    def receive_data(self, frame):
        print(f"[{self.name}] received DATA destined for IP {frame['l3']['dst_ip']}")
        print(f"[{self.name}] Message from {frame['l3']['src_ip']}: {frame['l3']['payload']}")

        # Learn sender MAC
        sender_ip = frame['l3']['src_ip']
        sender_mac = frame['l2']['src_mac']
        self.arp_table[sender_ip] = sender_mac
        print(f"[{self.name}] Learned {sender_ip} is at {sender_mac}")
        self.print_arp_table()

    def receive_arp_request(self, frame):
    # Learn sender's IP and MAC from ARP request
      sender_ip = frame['sender_ip']
      sender_mac = frame['sender_mac']
      self.arp_table[sender_ip] = sender_mac
      print(f"[{self.name}] Learned {sender_ip} is at {sender_mac} from ARP Request")
      
      target_ip = frame['target_ip']
      if target_ip == self.ip:
          print(f"[{self.name}] Received ARP Request for {self.ip}, sending ARP Reply")
          reply = {
              'type': 'ARP_REPLY',
              'sender_ip': self.ip,
              'sender_mac': self.mac,
              'target_ip': sender_ip,
              'target_mac': sender_mac
          }
          self.connected_switch.receive_frame(reply, self)


    def print_arp_table(self):
        print(f"[{self.name}] ARP Table: {self.arp_table}")
