import sys

from client import Client

SERVER_IP = '192.168.1.1'
SERVER_UDP_PORT = 10000
CLIENT_UDP_PORT = 10001
from c2c_controller import Client2ClientController

# def display_menu():
#     choice = input("PRESS ENTER TO SEE THE MENU: ")
#     return choice

def main():
    udp_bind_port = 3000  # Example UDP port
    # controller = Client2ClientController(udp_bind_port)
    # controller.start_udp_server()

    # server_host = input("Enter server IP address: ")
    client = Client(name="Rainbow", host='localhost', udp_port=udp_bind_port, tcp_port=0, server_host='172.30.35.72')
    client.start()

    # client.request_to_server("PUBLISH", ["text.txt", "sample.txt"])
    # client.request_to_server("REMOVE", "text.txt")
    while True:
        print("\nAvailable Commands:")
        print("1. Register with server")
        print("2. Deregister with server")
        print("3. Publish files to server")
        print("4. Remove files from server")
        print("5. Request file from peer")
        print("6. Update contact information")
        print("7. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            print("Registering with server...")
            client.request_to_server("REGISTER")
        elif choice == "2":
            print("Deregistering with server...")
            client.request_to_server("DE-REGISTER")
        elif choice == "3":
            print("Publishing files to server...")
            client.request_to_server("PUBLISH", ["text.txt", "sample.txt"])
        elif choice == "4":
            file_choice = "y"
            file_names = []
            while file_choice == "y":
                file_name = input("Enter file name: ")
                file_names.append(file_name)
                file_choice = input("Would you like to enter another file name? (y/n)")
            client.request_to_server("REMOVE", file_names)
            print("Removing files from server...")
        elif choice == "5":
            print("Requesting file from peer...")
            peer_ip = input("Enter peer IP: ")
            peer_port = input("Enter peer port: ")
            request_id = input("Enter request ID: ")
            file_name = input("Enter file name: ")
            client.request_file(peer_ip=peer_ip, peer_port=int(peer_port), request_id=request_id, file_name=file_name)
        elif choice == "6":
            ip_address = input("Enter the new IP address: ")
            port = input("Enter the new port: ")
            client.request_to_server("UPDATE-CONTACT", ip_address=ip_address, udp_port=port)
            print("Updating contact...")
        elif choice == "7":
            print("Exiting...")
            break
    sys.exit()

if __name__ == "__main__":
    main()
