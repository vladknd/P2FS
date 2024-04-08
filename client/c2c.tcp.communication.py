import socket
import threading

class Client2ClientTCPCommunication:
    def __init__(self, bind_ip='', bind_port=65432):
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.bind_ip, self.bind_port))
        self.server_socket.listen(5)  # listen for up to 5 connections

    def start_server(self):
        print(f"Starting TCP server on {self.bind_ip}:{self.bind_port}")
        accept_thread = threading.Thread(target=self._accept_connections)
        accept_thread.daemon = True
        accept_thread.start()

    def _accept_connections(self):
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Accepted connection from {address}")
            client_thread = threading.Thread(target=self._handle_client, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()

    def _handle_client(self, client_socket):
        # This method should be implemented to handle file reception.
        # For simplicity, let's just receive a simple message.
        try:
            message = client_socket.recv(1024).decode()
            print(f"Received: {message}")
        finally:
            client_socket.close()

    def send_file(self, target_ip, target_port, file_path):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect((target_ip, target_port))
                # This example will just send the file name for simplicity.
                file_name = file_path.split('/')[-1]
                sock.sendall(file_name.encode())
                print(f"Sent file name {file_name} to {target_ip}:{target_port}")
        except Exception as e:
            print(f"Error sending file: {e}")
