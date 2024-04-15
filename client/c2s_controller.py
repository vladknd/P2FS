import threading 

from c2s_udp import Client2ServerUDPCommunication

class Client2ServerController:
    def __init__(self, udp_bind_port):
        self.udp_comm = Client2ServerUDPCommunication(bind_port=udp_bind_port)
        self.udp_server_thread = None

    def start_udp_server(self):
        threading.Thread(target=self.udp_comm.listen_for_requests, args=(self.handle_udp_request,)).start()

    def handle_udp_request(self, data, addr):
        message_type, *args = data.split()
        if message_type == "REGISTER":
            name, ip, udp_port = args
            self.register(name, ip, udp_port)
        elif message_type == "DEREGISTER":
            name = args[0]
            self.deregister(name)

    def register(self, name, ip, udp_port):
        self.registration_service.register(name, ip, udp_port)

    def deregister(self, name):
        self.registration_service.deregister(name)
