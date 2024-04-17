import asyncio
import os 
import threading

from c2c_controller import Client2ClientController

def run_user_interface(controller):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    while True:
        print("\nOptions:")
        print("1. Request a file from a peer")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            peer_ip = input("Enter peer IP: ")
            peer_port = int(input("Enter peer port: "))
            file_name = input("Enter file name to request: ")
            asyncio.run_coroutine_threadsafe(
                controller.request_file(peer_ip, peer_port, file_name),
                loop
            )
        elif choice == '2':
            print("Exiting...")
            return  # Exit the interface and stop the program
        else:
            print("Invalid choice. Please try again.")

async def main():
    # udp_bind_port = int(os.getenv('PORT'))
    # print(f"UDP bind port: {udp_bind_port}")

    controller = Client2ClientController(udp_bind_port=3001)

    # Start the UDP server as a background task
    udp_task = asyncio.create_task(controller.start_udp_server()) 
    # Run user interface in a separate thread
    ui_thread = threading.Thread(target=run_user_interface, args=(controller))
    ui_thread.start()

    # Wait for the UDP task and UI thread to finish (UI thread should run indefinitely unless exited)
    await udp_task
    ui_thread.join()

if __name__ == "__main__":
    asyncio.run(main())



    