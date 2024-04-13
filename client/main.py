import sys

from client import Client

SERVER_IP = '192.168.1.1'
SERVER_UDP_PORT = 10000
CLIENT_UDP_PORT = 10001

def main():
    # udp_comm_service = UDPCommunicationService(bind_ip='0.0.0.0', bind_port=12345)
    # registration_service = RegistrationService(udp_comm_service, SERVER_IP, SERVER_UDP_PORT)
    # client2server_controller = Client2ServerController(registration_service)

    # # Initialize Client2Client components similarly.

    # # Example Usage
    # client2server_controller.register('Alice', '192.168.1.2', 12345)
    # # Proceed with client-to-client interactions.

    client = Client(name='Alice', host=SERVER_IP, port=SERVER_UDP_PORT, udp_port=CLIENT_UDP_PORT, tcp_port=10002)
