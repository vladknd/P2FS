import threading

from c2c_tcp import Client2ClientTCPCommunication
from c2c_udp import Client2ClientUDPCommunication
from c2s_udp import Client2ServerUDPCommunication

from services.file_service import FileService

class Client:
    def __init__(self, name, host, udp_port, tcp_port):
        self.name = name
        self.host = host
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.udp_comm = Client2ClientUDPCommunication(bind_port=udp_port)
        self.tcp_comm = Client2ClientTCPCommunication()
        self.tcp_server_thread = None
        self.request_number = 0
        self.server_host = 'localhost'
        self.server_port = 3001
        self.file_list = []
        self.clients_information = []

    def start(self):
        self.start_udp_server()
        self.start_tcp_server()
        # udp_thread = threading.Thread(target=self.start_udp_server)
        # udp_thread.start()

        # tcp_thread = threading.Thread(target=self.start_tcp_server)
        # tcp_thread.start()

    def handle_udp_request(self, data, addr):
        print("Handling UDP request")
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
        elif message_type == "FILE-REQ":
            rq_number = args[0]
            file_name = args[1]
            if FileService.file_exists(file_name):
                if FileService.prompt_user_confirmation():
                    tcp_port = self.start_tcp_server()
                    response = f"FILE-CONF {rq_number} {tcp_port}"
                else:
                    response = f"FILE-DENIED {rq_number} User denied the request."
            else:
                response = f"FILE-ERROR {rq_number} File does not exist."
            self.udp_comm.send_message(addr, response)

    def start_udp_server(self):
        threading.Thread(target=self.udp_comm.listen_for_requests, args=(self.handle_udp_request,)).start()

    # idk what this does
    def start_tcp_server(self):
        # if not self.tcp_server_thread:
        #     self.tcp_server_thread = threading.Thread(target=self.tcp_comm.start_server, args=(self.handle_tcp_connection,))
        #     self.tcp_server_thread.start()
        #     while not self.tcp_comm.server_port:
        #         pass  # Wait for the server to start and get a port
        return self.tcp_comm.server_port

    def request_file(self, peer_ip, peer_port, request_id, file_name):
        self.udp_comm.send_file_request((peer_ip, peer_port), request_id, file_name)

    def handle_udp_response(self, data, addr):
        # This method is called whenever a UDP response is received.
        print("Handling UDP response")
        message_type, rq_number, *args = data.split()
        if message_type == "FILE-CONF":
            tcp_port = int(args[0])  # Extracting the TCP port from the response
            self.initiate_file_transfer(self.pending_file_name, tcp_port)  # Pending file name is stored when request is made

    def initiate_file_transfer(self, file_name, tcp_port):
        self.tcp_comm.connect_and_send_file(file_name, ('<peer_ip>', tcp_port))  # Placeholder for peer's IP address

    def request_to_server(self, message_type, file_list=[]):
        self.request_number += 1
        if message_type == "REGISTER":
            print("REGISTER in client")
            self.udp_comm.send_message((self.server_host, self.server_port), self.construct_message(message_type, self.request_number, self.name, self.host, self.udp_port))
        elif message_type == "DE-REGISTER":
            self.udp_comm.send_message((self.server_host, self.server_port), self.construct_message(message_type, self.request_number, self.name))
        elif message_type == "PUBLISH":
            self.udp_comm.send_message((self.server_host, self.server_port), self.construct_message(message_type, self.request_number, self.name, file_list))
        elif message_type == "REMOVE":
            self.udp_comm.send_message((self.server_host, self.server_port), self.construct_message(message_type, self.request_number, self.name, file_list))
        else: 
            print("Invalid message type")

    def construct_message(self, message_type, *args):
        unpacked_args = list(args)
        return f"{message_type} {' '.join(map(str, unpacked_args))}"
