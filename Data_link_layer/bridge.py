import random

class Device:
    """Represents a network device with a randomly generated MAC address."""
    def __init__(self, device_id):
        self.device_id = device_id
        self.mac = self.generate_mac()
        self.data = None  # Stores received data

    def generate_mac(self):
        """Generates a random MAC address."""
        return ':'.join(f"{random.randint(0, 255):02X}" for _ in range(6))

    def __repr__(self):
        return f"Device-{self.device_id} | MAC: {self.mac}"


class Hub:
    """Simulates a network hub that connects multiple devices."""
    def __init__(self, hub_id):
        self.hub_id = hub_id
        self.devices = []  # List of connected devices
    
    def connect_device(self, device):
        """Connects a device to the hub."""
        self.devices.append(device)
        print(f"Connected {device} to Hub-{self.hub_id}")

    def broadcast(self, src_mac, data):
        """Broadcasts data to all connected devices except the sender."""
        for device in self.devices:
            if device.mac != src_mac:
                device.data = data
                print(f"Message broadcasted to {device.mac}")


class Bridge:
    """Simulates a network bridge that connects multiple hubs and forwards traffic based on MAC addresses."""
    def __init__(self):
        self.mac_table = {}  # {MAC -> Hub}
        self.ports = {}  # {Port -> Hub}
    
    def connect_hub(self, hub, port):
        """Connects a hub to a specific port."""
        if port in self.ports:
            print(f"Port {port} is already occupied! Try another port.")
            return
        
        self.ports[port] = hub
        print(f"Connected Hub-{hub.hub_id} to Port {port}")
    
    def receive_frame(self, src_mac, dest_mac, data):
        """Processes incoming frames and forwards them intelligently."""
        print(f"\nFrame received from {src_mac} -> {dest_mac}: {data}")
    
        src_hub = None
        for port, hub in self.ports.items():
            for device in hub.devices:
                if device.mac == src_mac:
                    src_hub = hub
                    break
            if src_hub:
                break
        """Outer loop (for port, hub in self.ports.items()):
        Iterates through all ports and their connected hubs.
        
        Inner loop (for device in hub.devices):
        Checks each device in the current hub to see if its MAC matches src_mac"""
        
        if not src_hub:
            print(f"Source MAC {src_mac} is unknown. Frame dropped.")
            return
    
        if src_mac not in self.mac_table:
            print(f"Learning MAC {src_mac} on hub {src_hub.hub_id}")
            self.mac_table[src_mac] = src_hub
    
        if dest_mac in self.mac_table:
            dest_hub = self.mac_table[dest_mac]
            print(f"Forwarding frame to Hub-{dest_hub.hub_id}")
            for device in dest_hub.devices:
                if device.mac == dest_mac:
                    device.data = data
                    print(f"Message delivered to {dest_mac}: {data}")
                    return
        else:
            print(f"MAC {dest_mac} not in table, broadcasting...")
            src_hub.broadcast(src_mac, data)

    def display_mac_table(self):
        """Displays the MAC address table."""
        print("\nBridge MAC Table:")
        for mac, hub in self.mac_table.items():
            print(f"🔹 MAC: {mac} -> Hub-{hub.hub_id}")


def bridge_simulation():
    """Runs the network bridge simulation."""
    bridge = Bridge()

    num_hubs = int(input("Enter number of hubs: "))
    hubs = [Hub(i+1) for i in range(num_hubs)]

    num_devices = int(input("Enter number of devices per hub: "))
    devices = [[Device(j+1 + i*num_devices) for j in range(num_devices)] for i in range(num_hubs)]
    """Creates a 2D list of devices where: Each row i represents devices for hub i, Each column j represents device j in that hub"""
    """devices = [
    [Device(1), Device(2), Device(3)],  # Hub 0's devices (IDs 1-3)
    [Device(4), Device(5), Device(6)]   # Hub 1's devices (IDs 4-6)"""

    for i in range(num_hubs):
        for device in devices[i]:
            hubs[i].connect_device(device)

    print("\nConnecting hubs to bridge:")
    for i, hub in enumerate(hubs):
        bridge.connect_hub(hub, i+1)
    
    """Device IDs are assigned sequentially across all hubs (e.g., with 2 hubs and 3 devices: Hub 1 gets devices 1,2,3; Hub 2 gets 4,5,6)"""
    
    print("\nSimulate Frame Transmission")
    while True:
        hub_idx = int(input("Enter source hub number: ")) - 1
        device_idx = int(input("Enter source device number: ")) - 1

        if hub_idx < 0 or hub_idx >= num_hubs or device_idx < 0 or device_idx >= num_devices:
            print("Invalid input! Try again.")
            continue

        src_device = devices[hub_idx][device_idx]

        hub_idx = int(input("Enter destination hub number: ")) - 1
        device_idx = int(input("Enter destination device number: ")) - 1

        if hub_idx < 0 or hub_idx >= num_hubs or device_idx < 0 or device_idx >= num_devices:
            print("Invalid input! Try again.")
            continue

        dest_device = devices[hub_idx][device_idx]

        message = input("Enter message to send: ")
        bridge.receive_frame(src_device.mac, dest_device.mac, message)

        cont = input("Do you want to send another frame? (y/n): ").lower()
        if cont != 'y':
            break

    bridge.display_mac_table()

if __name__ == "__main__":
    bridge_simulation()