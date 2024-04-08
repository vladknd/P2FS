class Client2ClientUDPCommunication:
    def __init__(self, bind_port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('', bind_port))

    def send_handshake(self, target_ip, target_port, message):
        self.socket.sendto(message.encode(), (target_ip, target_port))

    def listen_for_handshake(self):
        while True:
            message, address = self.socket.recvfrom(1024)
            print(f"Handshake received from {address}: {message.decode()}")
            # Process handshake message and respond or initiate TCP connection for file transfer
