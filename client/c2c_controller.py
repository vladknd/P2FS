import threading
from c2c_tcp import Client2ClientTCPCommunication
from c2c_udp import Client2ClientUDPCommunication

from services.file_service import FileService

class Client2ClientController:
    def __init__(self, udp_bind_port, tcp_listen_port=0):
        self.udp_comm = Client2ClientUDPCommunication(bind_port=udp_bind_port)
        self.tcp_comm = Client2ClientTCPCommunication()
        self.tcp_server_thread = None

    def handle_udp_request(self, data, addr):
        message_type, rq_number, file_name = data.split(maxsplit=2)
        if message_type == "FILE-REQ":
            if FileService.file_exists(file_name):
                if FileService.prompt_user_confirmation():
                    tcp_port = self.start_tcp_server()
                    response = f"FILE-CONF {rq_number} {tcp_port}"
                else:
                    response = f"FILE-DENIED {rq_number} User denied the request."
            else:
                response = f"FILE-ERROR {rq_number} File does not exist."
            self.udp_comm.send_response(addr, response)

    def start_udp_server(self):
        threading.Thread(target=self.udp_comm.listen_for_requests, args=(self.handle_udp_request,)).start()

    def start_tcp_server(self):
        if not self.tcp_server_thread:
            self.tcp_server_thread = threading.Thread(target=self.tcp_comm.start_server, args=(self.handle_tcp_connection,))
            self.tcp_server_thread.start()
            while not self.tcp_comm.server_port:
                pass  # Wait for the server to start and get a port
        return self.tcp_comm.server_port

    def handle_tcp_connection(self, conn):
        # Implement the logic to handle incoming file data or send file data
        pass

    def request_file(self, peer_ip, peer_port, request_id, file_name):
        self.udp_comm.send_file_request((peer_ip, peer_port), request_id, file_name)
