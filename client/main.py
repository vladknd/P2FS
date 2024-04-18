import socket
import asyncio
import os 
import threading
import concurrent

from c2c_controller import Client2ClientController

from c2c_udp import Client2ClientUDPCommunication
from c2c_tcp import Client2ClientTCPCommunication

def startup():
    name = input("Enter your name: ")
    server_host = input("Enter the server host: ")
    server_port = int(input("Enter the server port: "))
    return name, server_host, server_port

async def run_user_interface(controller): 
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
            await asyncio.create_task(controller.request_to_server("REGISTER"))
        elif choice == "2":
            print("Deregistering with server...")
            await asyncio.create_task(controller.request_to_server("DE-REGISTER"))
        elif choice == "3":
            print("Publishing files to server...")
            await asyncio.create_task(controller.request_to_server("PUBLISH", ["text.txt", "sample.txt"]))
        elif choice == "4":
            file_choice = "y"
            file_names = []
            while file_choice == "y":
                file_name = input("Enter file name: ")
                file_names.append(file_name)
                file_choice = input("Would you like to enter another file name? (y/n)")
            await asyncio.create_task(controller.request_to_server("REMOVE", file_names))
            print("Removing files from server...")
        elif choice == "5":
            print("Requesting file from peer...")
            peer_ip = input("Enter peer IP: ")
            peer_port = input("Enter peer port: ")
            request_id = input("Enter request ID: ")
            file_name = input("Enter file name: ")
            await asyncio.create_task(controller.request_file(peer_ip=peer_ip, peer_port=int(peer_port), request_id=request_id, file_name=file_name))
        elif choice == "6":
            ip_address = input("Enter the new IP address: ")
            port = input("Enter the new port: ")
            await asyncio.create_task(controller.request_to_server("UPDATE-CONTACT", ip_address=ip_address, udp_port=port))
            print("Updating contact...")
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

async def main():
    udp_bind_port = 3000
    # name, server_host, server_port = startup()
    loop = asyncio.get_running_loop()
    # Create a default executor
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    # udp_bind_port = int(os.getenv('PORT'))
    # print(f"UDP bind port: {udp_bind_port}")
    # local_ip = socket.gethostbyname(socket.gethostname())
    local_ip = "localhost"
    tcp = Client2ClientTCPCommunication()
    udp = Client2ClientUDPCommunication(loop, tcp, local_ip, udp_bind_port)
    controller = Client2ClientController(loop, udp, tcp)
    await asyncio.create_task(udp.start_server()) 
    
if __name__ == "__main__":
    asyncio.run(main())



    