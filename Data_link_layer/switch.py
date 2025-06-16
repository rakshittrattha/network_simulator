from Data_link_layer.frame import Frame
#The Switch class represents a network switch that can learn MAC addresses 
#and forward frames based on its MAC address table.
class Switch:
    def __init__(self):
        """ Initialize switch with an empty MAC address table. """
        self.mac_table = {}  # Dictionary to store MAC-to-port mappings

    def learn_mac(self, mac_address, port):
        """ Store the MAC address in the switch table. """
        self.mac_table[mac_address] = port
        print("\n========================================")
        print(f"[SWITCH] Learned MAC {mac_address} on port {port}")
        print("========================================\n")
        
        
    def display_mac_table(self):
        """ Display the current MAC address table. """
        print("\n========================================")
        print("          MAC ADDRESS TABLE             ")
        print("========================================")
        for mac_address, port in self.mac_table.items():
            print(f"MAC Address: {mac_address} -> Port: {port}")
        print("========================================\n")    
#The method checks if the destination MAC 
#address of the frame is in the mac_table dictionary
    def forward_frame(self, sender, receiver, data):
        """ Forward frame based on the MAC address table. """
        
        print("\n========================================")
        print(f"[SWITCH] Received Frame from {sender} to {receiver}")
        print("========================================\n")

        # Create a Frame object
        frame = Frame(sender, receiver, data)

        if frame.dest_mac in self.mac_table:
            port = self.mac_table[frame.dest_mac]
            print(f"\n[SWITCH] Forwarding frame to {frame.dest_mac} on port {port}\n")
        else:
            print("\n[SWITCH] Destination unknown, broadcasting...\n")
            for port in self.mac_table.values():
                print(f"  --> Broadcast on Port {port}")
            print("\n========================================\n")