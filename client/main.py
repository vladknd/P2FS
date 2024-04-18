import asyncio
import os 
import threading

from c2c_controller import Client2ClientController

from c2c_udp import Client2ClientUDPCommunication
from c2c_tcp import Client2ClientTCPCommunication

async def run_user_interface(loop, controller):
    while True:
        print("\nOptions:")
        print("1. Request a file from a peer")
        print("2. Exit")
        choice = await loop.run_in_executor(None, input, "Enter your choice: ")
        if choice == '1':
            await asyncio.create_task(controller.request_file('132.205.46.65', 3005, 'newfile')
    )
        elif choice == '2':
            print("Exiting...")
            return  # Exit the interface and stop the program
        else:
            print("Invalid choice. Please try again.")

async def main():
    loop = asyncio.get_running_loop()

    # udp_bind_port = int(os.getenv('PORT'))
    # print(f"UDP bind port: {udp_bind_port}")
    tcp = Client2ClientTCPCommunication()
    udp = Client2ClientUDPCommunication(loop, tcp, '127.0.0.1', 3005)
    await asyncio.create_task(udp.start_server()) 

    controller = Client2ClientController(udp, tcp, loop)

    await run_user_interface(loop, controller)
if __name__ == "__main__":
    asyncio.run(main())



    