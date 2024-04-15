import sys
import os 
import asyncio

from c2c_controller import Client2ClientController

async def main():
    # udp_bind_port = 3000  # Example UDP port
    udp_bind_port = int(os.getenv('PORT'))
    print(f"UDP bind port: {udp_bind_port}")
    controller = Client2ClientController(udp_bind_port)
    controller.start_udp_server()

    while True:
        print("\nAvailable Commands:")
        print("1. Request file from peer")
        print("2. Exit")
        choice = input("Enter your choice: ")
        if int(choice) == 1:   
            await controller.request_file(peer_ip='localhost', peer_port=3001, request_id=1, file_name="text.txt") # hard coded values
        elif int(choice) == 2:
            print("Exiting...")
            break
        else:
            print(type(int(choice)))
            print(int(choice))
            print('something went terribly wrong')
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())
