from c2c.tcp.communication import Client2ClientTCPCommunication
from c2c.udp.communication import Client2ClientUDPCommunication

class Client2ClientController:
    def __init__(self,udp_ip, udp_port, tcp_ip, tcp_port):
        self.udp_comm = Client2ClientUDPCommunication(udp_port)
        self.tcp_comm = Client2ClientTCPCommunication(tcp_port)

    def request_file(self, target_ip, target_udp_port, file_name):
        # Send FILE-REQ message
        message = f"FILE-REQ {self.tcp_comm.rq_number} {file_name}"
        self.udp_comm.send_message(message, (target_ip, target_udp_port))
        
        # Listen for FILE-CONF or FILE-ERROR
        response, _ = self.udp_comm.receive_message()
        if response.startswith("FILE-CONF"):
            _, _, tcp_socket = response.split()
            self.tcp_comm.send_file(file_name, target_ip, int(tcp_socket))
        elif response.startswith("FILE-ERROR"):
            print(f"File transfer error: {response}")

    def start_serving_files(self, process_request_callback):
        self.tcp_comm.start_server(process_request_callback)
