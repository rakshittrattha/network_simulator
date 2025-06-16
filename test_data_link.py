import sys
import os

# Ensure the parent directory is in the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#imports based on files in the data_link_layer folder
from Data_link_layer.frame import Frame
from Data_link_layer.switch import Switch
from Data_link_layer.access_control import CSMA_CD
from Data_link_layer.end_device import EndDevice

def test_case_1():
    # =========================================================
    # TEST CASE 1: SWITCH WITH 5 DEVICES & ACCESS CONTROL
    # =========================================================
    print("\n===== TEST CASE 1: SWITCH WITH 5 DEVICES =====")

    # Create a switch
    switch = Switch()

    # Create 5 end devices and connect to switch
    devices = [
        EndDevice("PC1", "AA:BB:CC:DD:EE:01"),
        EndDevice("PC2", "AA:BB:CC:DD:EE:02"),
        EndDevice("PC3", "AA:BB:CC:DD:EE:03"),
        EndDevice("PC4", "AA:BB:CC:DD:EE:04"),
        EndDevice("PC5", "AA:BB:CC:DD:EE:05"),
    ]

    # Learn MAC addresses in switch
    for i, device in enumerate(devices, start=1):
        switch.learn_mac(device.mac_address, i)

    # Display MAC table
    switch.display_mac_table()

    # Send data between devices
    frame1 = Frame(devices[0].mac_address, devices[3].mac_address, "Hello PC4!")
    devices[0].send_frame(frame1, switch)

    # Report Broadcast & Collision Domains
    print("\n===== NETWORK ANALYSIS =====")
    print("Number of Broadcast Domains: 1 (Single Switch Network)")
    print("Number of Collision Domains: 5 (Each device has its own connection)")


def test_case_2():
    # =========================================================
    # TEST CASE 2: TWO STAR TOPOLOGIES WITH HUBS + SWITCH
    # =========================================================
    print("\n===== TEST CASE 2: TWO STAR TOPOLOGIES WITH HUBS =====")

    class Hub:
        """Simulates a Hub that forwards frames to all connected devices."""
        def __init__(self, name):
            self.name = name
            self.devices = []

        def connect(self, device):
            """Connects an end device to the hub."""
            self.devices.append(device)

        def receive_frame(self, frame, sender):
            """Broadcasts frame to all connected devices."""
            print(f"\n[{self.name}] Broadcasting Frame: {frame.payload}")
            for device in self.devices:
                if device != sender:
                    device.receive_frame(frame)

    # Create two hubs
    hub1 = Hub("Hub1")
    hub2 = Hub("Hub2")

    # Create 5 devices for each hub
    hub1_devices = [EndDevice(f"Hub1_PC{i+1}", f"AA:BB:CC:DD:EE:1{i}") for i in range(5)]
    hub2_devices = [EndDevice(f"Hub2_PC{i+1}", f"AA:BB:CC:DD:EE:2{i}") for i in range(5)]

    # Connect devices to respective hubs :
    for device in hub1_devices:
        hub1.connect(device)

    for device in hub2_devices:
        hub2.connect(device)

    # Create a switch to connect the two hubs
    switch2 = Switch()

    # Connect hubs to the switch (assuming they act like a device)
    switch2.learn_mac("HUB1", 1)
    switch2.learn_mac("HUB2", 2)

    # Send data from a PC in Hub1 to a PC in Hub2
    frame2 = Frame(hub1_devices[0].mac_address, hub2_devices[3].mac_address, "Hello Hub2_PC4!")
    hub1.receive_frame(frame2, hub1_devices[0])
    switch2.forward_frame(frame2, "HUB1", frame2.payload)

    # Report Broadcast & Collision Domains
    print("\n===== NETWORK ANALYSIS =====")
    print("Number of Broadcast Domains: 2 (One per hub)")
    print("Number of Collision Domains: 5 per hub (Since hubs cause collisions)")
    print("Total Collision Domains: 10 (5 per hub)")


def test_case_3():
    # =========================================================
    # TEST CASE 3: TESTING CSMA/CD
    # =========================================================
    print("\n===== TEST CASE 3: TESTING CSMA/CD =====")

    csma_cd = CSMA_CD()

    # Test CSMA/CD with a sample frame transmission
    frame1 = Frame("AA:BB:CC:DD:EE:01", "AA:BB:CC:DD:EE:02", "Hello PC2!")
    csma_cd.send_frame(frame1)
    
test_case_1()