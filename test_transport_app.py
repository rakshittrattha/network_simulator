from TransportLayer.transport import TransportLayer
from ApplicationLayer.echo_app import echo_server, echo_client
from ApplicationLayer.ftp_app import ftp_server, ftp_client
from ApplicationLayer.telnet_app import telnet_server, telnet_client
import threading
import time

def simulate_transport_layer():
    channel = []
    transport = TransportLayer()

    print("\n" + "="*60)
    print("========== TRANSPORT & APPLICATION LAYER DEMO ==========")
    print("="*60)

    while True:
        print("\nSelect a service to simulate:")
        print("1. Echo")
        print("2. FTP")
        print("3. Telnet")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            # Echo Test
            print("\n" + "="*60)
            print("--- Echo Service Test ---")
            print("="*60)
            echo_port = transport.assign_port("echo_server", 7000)
            print(f"[Setup] Assigned port 7000 to Echo Server.")
            server_thread = threading.Thread(target=echo_server, args=(transport, echo_port, channel))
            server_thread.start()
            time.sleep(0.2)
            echo_client(transport, echo_port, "Hello, World!", channel)
            server_thread.join()
            print("[Result] Echo test completed.\n")

        elif choice == '2':
            # FTP Test
            print("\n" + "="*60)
            print("--- FTP Service Test ---")
            print("="*60)
            ftp_port = transport.assign_port("ftp_server", 21)
            files = {"readme.txt": "This is a test file."}
            print(f"[Setup] Assigned port 21 to FTP Server.")
            print(f"[Setup] Files available: {list(files.keys())}")
            ftp_server_thread = threading.Thread(target=ftp_server, args=(transport, ftp_port, channel, files))
            ftp_server_thread.start()
            time.sleep(0.2)
            ftp_client(transport, ftp_port, "readme.txt", channel)
            ftp_server_thread.join()
            print("[Result] FTP test completed.\n")

        elif choice == '3':
            # Telnet Test
            print("\n" + "="*60)
            print("--- Telnet Service Test ---")
            print("="*60)
            telnet_port = transport.assign_port("telnet_server", 23)
            print(f"[Setup] Assigned port 23 to Telnet Server.")
            telnet_server_thread = threading.Thread(target=telnet_server, args=(transport, telnet_port, channel))
            telnet_server_thread.start()
            time.sleep(0.2)
            telnet_client(transport, telnet_port, "date", channel)
            telnet_server_thread.join()
            print("[Result] Telnet test completed.\n")

        elif choice == '4':
            print("\nExiting Transport Layer simulation. Goodbye!\n")
            break

        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")
