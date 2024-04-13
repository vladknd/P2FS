import sys 
import socket
import threading
from controller import Controller 

class Server:
    def __init__(self, host='', port=3000):
        self.host = host
        self.port = port

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.bind((self.host, self.port))
        except socket.error as e:
            print('Failed to create/bind socket. Error Code : ' + str(e))
            sys.exit()
        print(f"Server listening on {self.host}:{self.port}")

    def start(self):
        try:
            while True:
                message, client_address = self.server_socket.recvfrom(4096)
                print(f"Received message from {client_address}")

                # Using the Controller to route the message to the appropriate handler
                thread = threading.Thread(target=Controller.route(message, client_address, self.server_socket))
        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            self.server_socket.close()

