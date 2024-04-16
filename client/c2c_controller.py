import threading
import asyncio

from c2c_tcp import Client2ClientTCPCommunication
from c2c_udp import Client2ClientUDPCommunication

from services.file_service import FileService

class Client2ClientController:
    def __init__(self, udp_bind_port, tcp_listen_port=0):
        self.udp_comm = Client2ClientUDPCommunication(bind_port=udp_bind_port)
        self.tcp_comm = Client2ClientTCPCommunication()
        self.tcp_server_thread = None

    async def handle_udp_request(self, data, addr):
        print(f"Received UDP request: {data} from {addr}")
        message_type, rq_number, file_name = data.split(maxsplit=2)
        if message_type == "FILE-REQ":
            if FileService.file_exists(file_name):
                confirmed = FileService.prompt_user_confirmation()
                if confirmed:
                    tcp_port = self.start_tcp_server()
                    print(f"FILE-CONF {rq_number} {tcp_port}")
                    response = f"FILE-CONF {rq_number} {tcp_port}"
                else:
                    print(f"FILE-DENIED {rq_number} User denied the request.")
                    response = f"FILE-DENIED {rq_number} User denied the request."
            else:
                print(f"FILE-ERROR {rq_number} File does not exist.")
                response = f"FILE-ERROR {rq_number} File does not exist."
            await self.udp_comm.send_message(addr, response)

    def start_udp_server(self):
        
        #seperated the thread initialisations and starting method 
        thread = threading.Thread(target=self.udp_comm.listen_for_requests, args=(self.handle_udp_request,))
        thread.start() # kept the thread and inputed a async function inside of it

    def start_tcp_server(self):
        if not self.tcp_server_thread:
            self.tcp_server_thread = threading.Thread(target=self.tcp_comm.start_server, args=(self.handle_tcp_connection,))
            self.tcp_server_thread.start()
            while not self.tcp_comm.server_port:
                pass  # Wait for the server to start and get a port
        return self.tcp_comm.server_port

    async def request_file(self, peer_ip, peer_port, request_id, file_name):
        await self.udp_comm.send_file_request((peer_ip, peer_port), request_id, file_name)

    def handle_udp_response(self, data, addr):
        # This method is called whenever a UDP response is received.
        message_type, rq_number, *args = data.split()
        if message_type == "FILE-CONF":
            tcp_port = int(args[0])  # Extracting the TCP port from the response
            self.initiate_file_transfer(self.pending_file_name, tcp_port)  # Pending file name is stored when request is made

    def initiate_file_transfer(self, file_name, tcp_port):
        self.tcp_comm.connect_and_send_file(file_name, ('<peer_ip>', tcp_port))  # Placeholder for peer's IP address