import asyncio
import socket
import os 
import aioconsole

class Client2ClientUDPCommunication:
    def __init__(self, loop, tcp, bind_ip='127.0.0.1', bind_port=3000):
        self.tcp_comm = tcp
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.loop = loop
        self.transport = None

    async def start_server(self):
        self.transport, _ = await self.loop.create_datagram_endpoint(
            lambda: self, 
            local_addr=(self.bind_ip, self.bind_port)
        )

        if self.transport is not None:
            print(f"UDP server initialized successfully on {self.bind_ip}:{self.bind_port}")
        else:
            print("Failed to initialize UDP server")

    async def handle_udp_request(self, data, addr):
        print(f"Received UDP data: {data} from {addr}")
        parts = data.split()
        header = parts[0]
        args = parts[1:]
        message_type, *args = data.split()
        
        if message_type == "REGISTERED":
            print("Registered with server")
        elif message_type == "REGISTER-DENIED":
            print("Registration denied")
        elif message_type == "PUBLISHED":
            print("Published files to server")
        elif message_type == "PUBLISH-DENIED":
            print("Publish denied")
        elif message_type == "REMOVED":
            print("Removed files from server")
        elif message_type == "REMOVE-DENIED":
            print("Remove denied")
        elif message_type == "UPDATE":
            print("Received update from server")
            print(args)
            self.clients_information = args
        elif message_type == "UPDATE-CONFIRMED":
            print("Received update contact from server")
            print(args)
            self.update_contacts(args)
        elif message_type == "UPDATE-DENIED":
            print("Update denied")
            print(args)
        elif header == "FILE-REQ":
            file_name = parts[2]
            await self.handle_file_request(file_name, addr)
        elif header == "FILE-CONF":
            tcp_port = int(parts[1])
            self.loop.run_in_executor(None, self.tcp_comm.receive_file, addr[0], tcp_port)
        else:
            print("Unknown header or message format.")

    def connection_made(self, transport):
        self.transport = transport
        print(f"UDP server started on {self.bind_ip}:{self.bind_port}")
    
    def error_received(self, exc):
        print(f"UDP error received: {exc}")

    def connection_lost(self, exc):
        print("UDP connection closed")
        if exc:
            print(f"UDP connection error: {exc}")
            
    def datagram_received(self, data, addr):
        message = data.decode()
        print(f"Received UDP data: {message} from {addr}")
        asyncio.create_task(self.handle_udp_request(message, addr))

    async def send_message(self, addr, message):
        if not self.transport:
            print("Transport not initialized, message not sent")
            return  # Prevents trying to send message if transport is not available
        print(f"Sending UDP message: {message} to {addr}")
        self.transport.sendto(message.encode(), addr)
        print(f"Sent UDP message: {message} to {addr}")

    async def handle_file_request(self, file_name, addr):
        file_path = f"./files/{file_name}.txt"
        print(f"Request to send file: {file_name}")
        
        # Print the files available in the path
        files = os.listdir("./files")
        print("Available files:")
        for file in files:
            print(file)

        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"File {file_name} does not exist.")
            response = "FILE-DENIED"
            await self.send_message(addr, response)
            return

        # confirmation = await aioconsole.ainput("Confirm file send (y/n): ")
        confirmation = await aioconsole.ainput("Confirm file send (y/n): ")

        if confirmation.strip().lower() == "y":
        # else:
            tcp_port = self.tcp_comm.find_free_port()
            response = f"FILE-CONF {tcp_port}"
            print(f"Sending file {file_name} to {addr} on port {tcp_port}")
            await self.send_message(addr, response)
            print(f"Sending file {file_name} to {addr} on port {tcp_port}")
            self.loop.run_in_executor(None, self.tcp_comm.send_file, file_name, tcp_port)

        else:
            response = "FILE-DENIED"
            await self.send_message(addr, response)

    def update_contacts(self, args):
        request_number, name, ip_address, udp_port = args
        self.host = ip_address
        self.udp_port = udp_port
        print(f"Updated contact: {name} {ip_address} {udp_port}")

    