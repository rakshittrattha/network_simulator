#The EndDevice class represents a network device that can send and receive frames.
class EndDevice:
    """Represents an end device that can send and receive frames."""
    def __init__(self, name, mac_address):
        self.name = name
        self.mac_address = mac_address

    def receive_frame(self, frame):
        """Receives and prints frame details."""
        print(f"\n[DEVICE: {self.name}] Received Frame: {frame.payload}\n")

    def send_frame(self, frame, switch):
        """Sends a frame through the switch."""
        print(f"\n[DEVICE: {self.name}] Sending Frame: {frame.payload} --> {frame.dest_mac}\n")
        switch.forward_frame(frame, self.mac_address,frame.payload)






























# class EndDevice:
#     def __init__(self, name, mac):
#         self.name = name
#         self.mac = mac

#     def receive_frame(self, frame):
#         print(f"{self.name} received frame: {frame}")