import socket
import asyncio
import aioconsole
import os 
import threading

from c2c_controller import Client2ClientController

from c2c_udp import Client2ClientUDPCommunication
from c2c_tcp import Client2ClientTCPCommunication

async def startup():
    name = input("Enter the name: ")
    server_host = input("Enter the server host: ")
    server_port = int(input("Enter the server port: "))
    return name, server_host, server_port

async def run_user_interface(loop, controller): 
    while True:
        print("\nAvailable Commands:")
        print("1. Register with server")
        print("2. Deregister with server")
        print("3. Publish files to server")
        print("4. Remove files from server")
        print("5. Request file from peer")
        print("6. Update contact information")
        print("7. Exit")
        # choice = await loop.run_in_executor(None, input, "Enter your choice: ")
        choice = await aioconsole.ainput("Enter your choice: ")

        if choice == "1":
            print("Registering with server...")
            await asyncio.create_task(controller.request_to_server("REGISTER"))
        elif choice == "2":
            print("Deregistering with server...")
            await asyncio.create_task(controller.request_to_server("DE-REGISTER"))
        elif choice == "3":
            print("Publishing files to server...")
            file_choice = "y"
            file_names = []
            while file_choice == "y":
                file_name = await aioconsole.ainput("Enter file name: ")
                file_names.append(file_name)
                file_choice = await aioconsole.ainput("Would you like to enter another file name? (y/n)")
            await asyncio.create_task(controller.request_to_server("PUBLISH", file_names))
        elif choice == "4":
            
            print("Removing files from server...")
        elif choice == "5":
            print("Requesting file from peer...")
            peer_ip = await aioconsole.ainput("Enter peer IP: ")
            peer_port = await aioconsole.ainput("Enter peer port: ")
            file_name = await aioconsole.ainput("Enter file name: ")
            await asyncio.create_task(controller.request_file(peer_ip=peer_ip, peer_port=int(peer_port), file_name=file_name))
        elif choice == "6":
            ip_address = await aioconsole.ainput("Enter the new IP address: ")
            port = await aioconsole.ainput("Enter the new port: ")
            await asyncio.create_task(controller.request_to_server("UPDATE-CONTACT", ip_address=ip_address, udp_port=port))
            print("Updating contact...")
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

async def main():
    udp_bind_port = 3002
    name, server_host, server_port = await startup()
    loop = asyncio.get_running_loop()
    # udp_bind_port = int(os.getenv('PORT'))
    # print(f"UDP bind port: {udp_bind_port}")
    local_ip = socket.gethostbyname(socket.gethostname())
    # local_ip = "localhost"
    tcp = Client2ClientTCPCommunication()
    udp = Client2ClientUDPCommunication(loop, tcp, local_ip, udp_bind_port)
    controller = Client2ClientController(loop, udp, tcp, name, server_host, server_port)
    await asyncio.create_task(udp.start_server()) 
    await asyncio.create_task(run_user_interface(loop, controller))
    
if __name__ == "__main__":
    asyncio.run(main())



    