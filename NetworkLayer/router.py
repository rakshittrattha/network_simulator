import ipaddress

class RIPProtocol:
    def __init__(self, router_id):
        self.router_id = router_id
        self.neighbors = {}  # neighbor_id -> cost (ditectly connected)
        self.routing_table = {self.router_id: (0, self.router_id)}  # destination -> (cost, next_hop) --> Stores the best known paths to all destinations

    def add_neighbor(self, neighbor_id, cost): # direct connection between the routers
        self.neighbors[neighbor_id] = cost # --> Adds a neighbor to the routers neighbor list
        self.routing_table[neighbor_id] = (cost, neighbor_id) # --> Adds the neighbor to the routing table

    def receive_vector(self, from_router, vector):
     updated = False
     cost_to_neighbor = 1  # RIP always assumes hop count of 1 (direct)
 
     for dest_router, (cost, _) in vector.items():
         if dest_router == self.router_id:
             continue  # Skip routes to self
 
         new_cost = cost + cost_to_neighbor
 
         if dest_router not in self.routing_table:
             self.routing_table[dest_router] = (new_cost, from_router)
             print(f"  {self.router_id}: added route to {dest_router} via {from_router}, cost {new_cost}")
             updated = True
         else:
             current_cost, current_next_hop = self.routing_table[dest_router]
             if new_cost < current_cost:
                 self.routing_table[dest_router] = (new_cost, from_router)
                 print(f"  {self.router_id}: updated route to {dest_router}, new cost {new_cost}, via {from_router}")
                 updated = True
 
     return updated

    def send_vector(self):
        return self.routing_table.copy()

    def get_next_hop(self, destination): #Given a destination, which immediate neighbor should I forward packets to
        return self.routing_table.get(destination, (float('inf'), None))[1] # [1] is the next hop, [0] is the cost (indexing)
        #default returns (inf, none)

    def print_routing_table(self):
        print(f"[RIP-{self.router_id}] Routing Table:")
        for dest, (cost, next_hop) in sorted(self.routing_table.items()):
            print(f"  Destination: {dest}, Cost: {cost}, Next Hop: {next_hop}")
        print()


def get_network(ip, prefix):
    return str(ipaddress.ip_network(f"{ip}/{prefix}", strict=False).network_address)
#strict=False means it won't error if the IP isn't the network address itself.



class Router:
    def __init__(self, name, interfaces):
        self.name = name
        self.interfaces = interfaces  # iface -> (ip, mac, prefix)
        self.arp_table = {} #IP->MAC
        self.routing_table = {}  # (network, prefix) -> iface
        self.interface_links = {}# iface -> (link_type, link_obj,peer_iface)
        self.pending_packets = {}#IP -> (frame, out_iface)
        self.rip = RIPProtocol(router_id=self.name)

        for iface, (ip, mac, prefix) in interfaces.items():
            network = get_network(ip, prefix)
            self.routing_table[(network, prefix)] = iface

        print(f"[{self.name}] Routing Table: {self.routing_table}")

    
    def add_directly_connected_to_rip(self):
     for iface, (ip, _, prefix) in self.interfaces.items():
         network = get_network(ip, prefix)
         network_id = f"{network}/{prefix}"
         self.rip.routing_table[network_id] = (0, self.name)
         


    def connect_interface(self, iface, link, peer_iface=None):
        #If peer_iface is given, it's a serial link connecting two routers.
        if peer_iface:
            self.interface_links[iface] = ('serial', link, peer_iface)
        else:
            self.interface_links[iface] = ('switch', link)

    def receive(self, frame, iface):
        if frame['type'] == 'DATA':
            self.receive_data(frame)
        elif frame['type'] == 'ARP_REQUEST':
            self.receive_arp_request(frame)
        elif frame['type'] == 'ARP_REPLY':
            self.receive_arp_reply(frame)

    def receive_arp_request(self, frame):
        target_ip = frame['target_ip']
        for iface, (ip, mac, _) in self.interfaces.items():
            if target_ip == ip:
                print(f"[{self.name}] received ARP Request for {target_ip} on {iface}, replying directly...")
                self.arp_table[frame['sender_ip']] = frame['sender_mac']
                self.print_arp_table()
                reply = {
                    'type': 'ARP_REPLY',
                    'sender_ip': ip,
                    'sender_mac': mac,
                    'target_ip': frame['sender_ip'],
                    'target_mac': frame['sender_mac']
                }
                link_type, *link_data = self.interface_links[iface]
                if link_type == 'switch':
                    link_data[0].receive_frame(reply, self)
                elif link_type == 'serial':
                    link_data[0].transmit(self, reply, iface)

    def receive_arp_reply(self, frame):
        print(f"[{self.name}] received ARP Reply: {frame['sender_ip']} is at {frame['sender_mac']}")
        self.arp_table[frame['sender_ip']] = frame['sender_mac']
        self.print_arp_table()
        if frame['sender_ip'] in self.pending_packets:
            pending_frame, out_iface = self.pending_packets.pop(frame['sender_ip'])
            out_ip, out_mac_self, _ = self.interfaces[out_iface]
            dst_mac = frame['sender_mac']
            pending_frame['l2'] = {'src_mac': out_mac_self, 'dst_mac': dst_mac}
            print(f"[{self.name}] prepares L2 header: src_mac={out_mac_self}, dst_mac={dst_mac}")
            print(f"[{self.name}] forwarding DATA to {pending_frame['l3']['dst_ip']} via MAC {dst_mac}")
            link_type, *link_data = self.interface_links[out_iface]
            if link_type == 'switch':
                link_data[0].receive_frame(pending_frame, self)

    def receive_data(self, frame):
        print(f"[{self.name}] received data frame. Stripping L2 and inspecting IP packet...")
        src_ip = frame['l3']['src_ip']
        dst_ip = frame['l3']['dst_ip']
        print(f"[{self.name}] IP Packet: src={src_ip}, dst={dst_ip}")

        best_match = None
        best_prefix = -1
        dst_ip_obj = ipaddress.IPv4Address(dst_ip)

        for (net_str, prefix), iface in self.routing_table.items():
            network = ipaddress.IPv4Network(f"{net_str}/{prefix}", strict=False)
            if dst_ip_obj in network and prefix > best_prefix:
                best_match = iface
                best_prefix = prefix

        if best_match:
            iface = best_match
            ip, mac, _ = self.interfaces[iface]
            link_type, *link_data = self.interface_links.get(iface, (None,))
            #link data mai switch ya serial hoga
            if link_type == 'switch':
                dst_mac = self.arp_table.get(dst_ip)
                if dst_mac is None:
                     print(f"[{self.name}] needs MAC of {dst_ip}, sending ARP Request on {iface}")
                     self.pending_packets[dst_ip] = (frame, iface)
                     arp_req = {
                         'type': 'ARP_REQUEST',
                         'sender_ip': ip,
                         'sender_mac': mac,
                         'target_ip': dst_ip
                     }
                     link_data[0].receive_frame(arp_req, self)
                else:
                    print(f"[{self.name}] MAC for {dst_ip} is {dst_mac}, forwarding data")
                    frame['l2'] = {'src_mac': mac, 'dst_mac': dst_mac}
                    print(f"[{self.name}] prepares L2 header: src_mac={mac}, dst_mac={dst_mac}")
                    print(f"[{self.name}] forwarding DATA to {dst_ip} via MAC {dst_mac}")
                    link_data[0].receive_frame(frame, self)

            elif link_type == 'serial':
                print(f"[{self.name}] forwarding frame over serial on {iface}")
                link_data[0].transmit(self, frame, iface)
        else:
            print(f"[{self.name}] No route to {dst_ip} found in routing table")

    def print_arp_table(self):
        print(f"[{self.name}] ARP Table: {self.arp_table}")


    def add_rip_neighbor(self, neighbor_router, cost):
        self.rip.add_neighbor(neighbor_router.name, cost)

    def exchange_routing_info(self, neighbor_router):
        updated = neighbor_router.rip.receive_vector(self.name, self.rip.send_vector())
        return updated

    def print_arp_table(self):
        print(f"[{self.name}] ARP Table: {self.arp_table}")


#clear static routes





def run_rip_simulation(routers, max_iterations=15):
    router_lookup = {router.name: router for router in routers}

    for i in range(max_iterations):
        print(f"\n--- RIP ROUND {i+1} ---")
        updated = False

        for router in routers:
            for neighbor_id in router.rip.neighbors:
                neighbor = router_lookup[neighbor_id]
                print(f"{router.name} receiving vector from {neighbor_id}")
                was_updated = router.rip.receive_vector(neighbor_id, neighbor.rip.routing_table)
                if was_updated:
                    print(f"{router.name}'s table updated using data from {neighbor_id}")
                updated |= was_updated

        if not updated:
            print("RIP tables converged.\n")
            break

    # Final RIP tables
    for router in routers:
        print(f"\nRouter {router.name} RIP Table:")
        router.rip.print_routing_table()



