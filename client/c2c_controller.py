import asyncio
import socket

from c2c_udp import Client2ClientUDPCommunication
from c2c_tcp import Client2ClientTCPCommunication

class Client2ClientController:
    def __init__(self, udp_bind_port):
        self.udp_comm = Client2ClientUDPCommunication(bind_port=udp_bind_port)
        self.tcp_comm = Client2ClientTCPCommunication()
        self.loop = asyncio.get_event_loop()

    async def handle_udp_request(self, data, addr):
        print(f"Received UDP data: {data} from {addr}")
        parts = data.split()
        header = parts[0]
        
        if header == "FILE-REQ":
            file_name = parts[1]
            await self.handle_file_request(file_name, addr)
        elif header == "FILE-CONF":
            tcp_port = int(parts[1])
            self.loop.run_in_executor(None, self.tcp_comm.receive_file, addr[0], tcp_port)
        else:
            print("Unknown header or message format.")

    async def handle_file_request(self, file_name, addr):
        file_path = f"./files/{file_name}.txt"
        print(f"Request to send file: {file_name}")
        
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"File {file_name} does not exist.")
            response = "FILE-DENIED"
            await self.udp_comm.send_message(addr, response)
            return
        
        confirmation = await self.get_user_confirmation()
        if confirmation.lower() == "yes":
            tcp_port = self.find_free_port()
            response = f"FILE-CONF {tcp_port}"
            await self.udp_comm.send_message(addr, response)
            self.loop.run_in_executor(None, self.tcp_comm.send_file, file_name, tcp_port)

        else:
            response = "FILE-DENIED"
            await self.udp_comm.send_message(addr, response)

    async def get_user_confirmation(self):
        print("Confirm file send (yes/no): ")
        return input().strip()

    def find_free_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            return s.getsockname()[1]

    async def start_udp_server(self):
        await self.udp_comm.listen_for_requests(self.handle_udp_request)

    async def request_file(self, peer_ip, peer_port, file_name):
        message = f"FILE-REQ {file_name}"
        await self.udp_comm.send_message((peer_ip, peer_port), message)
