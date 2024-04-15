import socket
import asyncio


class Client2ClientUDPCommunication:
    def __init__(self, bind_ip='127.0.0.1', bind_port=3000):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((bind_ip, bind_port))

    async def send_file_request(self, peer_address, request_id, file_name):
        print('we got here somehow')
        message = f"FILE-REQ {request_id} {file_name}"
        print(f"Sending file request: {message}")
        print(f"Peer address: {peer_address}")
        self.socket.sendto(message.encode(), peer_address)
        print("File request sent.")
        await asyncio.sleep(0.1)

    def listen_for_requests(self, handle_request_callback):
        print(f"Listening for UDP requests on port {self.socket.getsockname()[1]}...") # async stuff 
        while True:
            data, addr = self.socket.recvfrom(1024)
            handle_request_callback(data.decode(), addr)
            

    async def send_response(self, addr, response):
        self.socket.sendto(response.encode(), addr)
        await asyncio.sleep(0.1)
