import asyncio
import socket
import os 

class Client2ClientController:
    def __init__(self, loop, udp, tcp, name, server_host, server_port):
        self.udp_comm = udp
        self.tcp_comm = tcp
        self.loop = loop
        self.name = name
        self.server_host = server_host
        self.server_port = server_port
        self.request_number = 0
        self.clients_information = []

    async def request_file(self, peer_ip, peer_port, file_name):
        print(f"Requesting file: {file_name} from {peer_ip}:{peer_port}")
        message = f"FILE-REQ 1 {file_name}"
        await self.udp_comm.send_message((peer_ip, peer_port), message)


    async def request_to_server(self, message_type, file_list=[], ip_address=None, udp_port=None):
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
        elif message_type == "UPDATE-CONTACT":
            ip_address = ip_address if ip_address else self.host
            udp_port = udp_port if udp_port else self.udp_port
            self.udp_comm.send_message((self.server_host, self.server_port), self.construct_message(message_type, self.request_number, self.name, ip_address, udp_port))
        else: 
            print("Invalid message type")

    def construct_message(self, message_type, *args):
        unpacked_args = list(args)
        return f"{message_type} {' '.join(map(str, unpacked_args))}"