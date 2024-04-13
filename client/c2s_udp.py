import socket

class Client2ServerUDPCommunication:
    def __init__(self, bind_ip='', bind_port=None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if bind_port is not None:
            self.socket.bind((bind_ip, bind_port))

    def send_message(self, message, address):
        self.socket.sendto(message.encode(), address)

    def receive_message(self, buffer_size=1024):
        return self.socket.recvfrom(buffer_size)