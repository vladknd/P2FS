import asyncio
import socket
import os 

class Client2ClientController:
    def __init__(self, udp, tcp, loop):
        self.udp_comm = udp
        self.tcp_comm = tcp
        self.loop = loop

    async def request_file(self, peer_ip, peer_port, file_name):
        print(f"Requesting file: {file_name} from {peer_ip}:{peer_port}")
        message = f"FILE-REQ 1 {file_name}"
        await self.udp_comm.send_message((peer_ip, peer_port), message)
