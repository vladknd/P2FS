import asyncio
import socket

class Client2ClientUDPCommunication:
    def __init__(self, bind_ip='127.0.0.1', bind_port=3000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((bind_ip, bind_port))

    async def send_message(self, addr, message):
        self.socket.sendto(message.encode(), addr)
        print(f"Sent UDP message: {message} to {addr}")

    async def listen_for_requests(self, handle_request_callback):
        print(f"Listening for UDP requests on port {self.socket.getsockname()[1]}...")
        while True:
            data, addr = self.socket.recvfrom(1024)
            await handle_request_callback(data.decode(), addr)
