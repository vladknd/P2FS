import socket

class Client2ClientUDPCommunication:
    def __init__(self, bind_ip='0.0.0.0', bind_port=3001):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((bind_ip, bind_port))

    def send_file_request(self, peer_address, request_id, file_name):
        message = f"FILE-REQ {request_id} {file_name}"
        self.socket.sendto(message.encode(), peer_address)

    def listen_for_requests(self, handle_request_callback):
        print("Listening for UDP requests...")
        while True:
            data, addr = self.socket.recvfrom(1024)
            handle_request_callback(data.decode(), addr)

    def send_response(self, addr, response):
        self.socket.sendto(response.encode(), addr)
