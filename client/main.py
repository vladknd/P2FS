import socket
import asyncio
import os 
import threading

from c2c_controller import Client2ClientController

from c2c_udp import Client2ClientUDPCommunication
from c2c_tcp import Client2ClientTCPCommunication

def startup():
    name = input("Enter your name: ")
    server_host = input("Enter the server host: ")
    server_port = int(input("Enter the server port: "))
    return name, server_host, server_port

async def run_user_interface(loop, controller): 
    while True:
        print("\nOptions:")
        print("1. Request a file from a peer")
        print("2. Exit")
        choice = await loop.run_in_executor(None, input, "Enter your choice: ")
        if choice == '1':
            await asyncio.create_task(controller.request_file('132.205.46.65', 3005, 'newfile'))
        elif choice == '2':
            print("Exiting...")
            return  # Exit the interface and stop the program
        else:
            print("Invalid choice. Please try again.")

async def main():
    udp_bind_port = 3000
    name, server_host, server_port = startup()
    loop = asyncio.get_running_loop()
    # udp_bind_port = int(os.getenv('PORT'))
    # print(f"UDP bind port: {udp_bind_port}")
    local_ip = socket.gethostbyname(socket.gethostname())
    tcp = Client2ClientTCPCommunication()
    udp = Client2ClientUDPCommunication(loop, tcp, local_ip, udp_bind_port)
    await asyncio.create_task(udp.start_server()) 
    controller = Client2ClientController(loop, udp, tcp)
    await run_user_interface(loop, controller)

    
if __name__ == "__main__":
    asyncio.run(main())



    