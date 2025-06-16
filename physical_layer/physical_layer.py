import random

class EndDevice:
    """Simulates an End Device in the physical layer"""

    def generate_mac_address(): #12-digit hexadecimal number
        mac_address = [f"{random.randint(0x00, 0xFF):02X}" for _ in range(5)]
        return "00:" + ":".join(mac_address)

    def __init__(self, ip, port, data, seq_no):
        self.ip = ip
        self.mac = EndDevice.generate_mac_address()
        self.port = port  # used to simulate connection status; 0 means free
        self.data = data
        self.seq_no = seq_no #a unique identifier assigned to each element
        # to track the order of data packets or messages, especially in scenarios
        # where data might be transmitted out of order or lost.
        self.message = ""
        self.device_id = seq_no

    def display(self):
        print("IP Address    :", self.ip)
        print("MAC Address   :", self.mac)
        print("Port Value    :", self.port)

e1 = EndDevice(" 192.168.56.1", 0, "No data", 1)
e2 = EndDevice(" 192.168.56.2", 0, "No data", 2)
e3 = EndDevice(" 192.168.56.3", 0, "No data", 3)
e4 = EndDevice(" 192.168.56.4", 0, "No data", 4)
e5 = EndDevice(" 192.168.56.5", 0, "No data", 5)
e6 = EndDevice(" 192.168.56.6", 0, "No data", 6)
e7 = EndDevice(" 192.168.56.7", 0, "No data", 7)
e8 = EndDevice(" 192.168.56.8", 0, "No data", 8)
e9 = EndDevice(" 192.168.56.9", 0, "No data", 9)
e10 = EndDevice(" 192.168.56.10", 0, "No data", 10)

# index 0 is dummy - for 1-based access(means no end device  for 0)
endDevices = [-1, e1, e2, e3, e4, e5, e6, e7, e8, e9, e10]

# Function to check if any end device has vacant port (i.e. port == 0) if 1 mwans The device is already connected to another device
def end_device_vacant():
    for device in endDevices[1:]:
        if device.port == 0:
            return True
    return False
class Hub:
    def __init__(self):
        self.port1 = 0
        self.port2 = 0
        self.port3 = 0
        self.port4 = 0
        self.port5 = 0

    def hub_vacant(self):
        return self.port1 == 0 or self.port2 == 0 or self.port3 == 0 or self.port4 == 0 or self.port5 == 0
class Connection:
    def __init__(self, sender: EndDevice, receiver: EndDevice):
        self.sender = sender
        self.receiver = receiver
        self.connected = False

    def make_connection(self):
        if self.sender.port == 0 and self.receiver.port == 0:
            self.sender.port = 1  # Assign ports
            self.receiver.port = 2
            self.connected = True
            print("Connection Made between two End Devices")
        else:
            print("No connection possible, one or both ports already occupied")

    def transmit_message(self, message: str):
        if not self.connected:
            print("Connection not established. Cannot transmit message.")
            return

        self.sender.data = message
        self.receiver.data = self.sender.data

        print("Message : ", message)
        print("Message sent successfully : ", self.receiver.data)

        if self.receiver.data == self.sender.data:
            print(f"         ---TRANSMISSION SUCCESSFULL---ACK RECEIVED FROM END DEVICE {self.receiver.device_id} ---")
        else:
            print("---ACK LOST---")


def simulate_dedicated_link():
        sender_id = int(input("Enter Sender Device no:(1-10) "))
        receiver_id = int(input("Enter Receiver Device no:(1-10) "))

        sender = endDevices[sender_id]
        receiver = endDevices[receiver_id]

        print(f"You have selected these two End Devices: {sender.device_id} and {receiver.device_id}")

        conn = Connection(sender, receiver)
        conn.make_connection()

        message = input("Enter the message to be transmitted: ")
        conn.transmit_message(message)
def simulate_star_topology():
    Hub1 = Hub()

    print("Enter Sender Device no(1-5):")
    sender_id = int(input())
    print("Enter Receiver Device no(2-5):")
    receiver_id = int(input())
    
    if sender_id < 1 or sender_id > 5 or receiver_id < 1 or receiver_id > 5:
        print("Invalid device number. Please enter a number between 1 and 5.")
        return

    if sender_id == receiver_id:
        print("Sender and Receiver cannot be the same device.")
        return
    
    print(f"You have selected these two End Devices within same HUB: {sender_id} and {receiver_id}")

    sender = endDevices[sender_id]
    receiver = endDevices[receiver_id]
#The sender device's port is vacant.The hub has at least one free port.
    if sender.port == 0 and Hub1.hub_vacant():
        print("Connection made between Sender-End Device and HUB")
        sender.port = 1
        #port1 is for input .Connect Sender to Hub always on port1
        Hub1.port1 = 9
# check whether the hub still has other ports available to connect to other devices .BROADCAST
#port2, port3, etc., are for outputs (from hub to other devices)
        if Hub1.port2 == 0 and Hub1.port3 == 0 and Hub1.port4 == 0 and Hub1.port5 == 0:
            print("Connection made between Hub and other End Devices")
            print("Enter the message:")
            message = input()
            print("Message: ", message)

            sender.data = message
            # Broadcast to all other end devices
            for i in range(2, 6):
                endDevices[i].data = sender.data
                print(f"Message sent to End Device {i} successfully: {endDevices[i].data}")

            # Simulate port values.marked them as occupied
            endDevices[2].port = 7
            endDevices[3].port = 2
            endDevices[4].port = 5
            endDevices[5].port = 62
            Hub1.port2 = 5
            Hub1.port3 = 8
            Hub1.port4 = 4
            Hub1.port5 = 1

            if receiver_id in [2, 3, 4, 5]:
                print(f"---ACK RECEIVED from End Device {receiver_id}---")
            else:
                print("ACK lost, no connection")
        else:
            print("No port vacant in HUB")
    else:
        print("---No port available in HUB or Sender already connected---")
"""def main():
         print("\n========== NETWORK SIMULATOR MENU ==========")
         print("1. Dedicated Link (End-to-End Connection)")
         print("2. Simulation through Hub — STAR TOPOLOGY")
         print("============================================")

         choice = int(input("Enter your choice (1 or 2): "))

         if choice == 1:
             print("\n[ Dedicated Link Simulation Selected ]")
             simulate_dedicated_link()

         elif choice == 2:
             print("\n[ Star Topology via Hub Simulation Selected ]")
             simulate_star_topology()

         else:
             print(" Invalid choice. Please enter 1 or 2.")

main()"""
