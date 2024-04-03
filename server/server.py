import socket
from controller import Controller  # Ensure this import path matches your project structure

class UDPServer:
    def __init__(self, host='localhost', port=3000):
        """
        Initializes the server with the given host and port.
        
        :param host: The hostname or IP address to listen on.
        :param port: The port number to listen on.
        """
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind((self.host, self.port))
        print(f"Server listening on {self.host}:{self.port}")

    def start(self):
        """
        Starts the server, listening for incoming messages and routing them.
        """
        try:
            while True:
                message, client_address = self.server_socket.recvfrom(4096)
                print(f"Received message from {client_address}")

                # Using the Controller to route the message to the appropriate handler
                Controller.route(message, client_address, self.server_socket)
        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            self.server_socket.close()

