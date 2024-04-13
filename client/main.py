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
    udp_bind_port = 80  # Example UDP port
    controller = Client2ClientController(udp_bind_port)
    controller.start_udp_server()

    while True:
        print("\nAvailable Commands:")
        print("1. Request file from peer")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":   
            peer_ip = input("Enter peer IP: ")
            peer_port = input("Enter peer port: ")
            request_id = input("Enter request ID: ")
            file_name = input("Enter file name: ")
            controller.request_file(peer_ip=peer_ip, peer_port=int(peer_port), request_id=request_id, file_name=file_name)
        elif choice == "2":
            print("Exiting...")
            break
    sys.exit()

if __name__ == "__main__":
    main()
