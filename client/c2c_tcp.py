import socket
import threading

class Client2ClientTCPCommunication:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_port = None

    def start_server(self, handle_connection_callback):
        self.server_socket.bind(('0.0.0.0', 0))  # Let OS pick the port
        self.server_socket.listen(1)
        self.server_port = self.server_socket.getsockname()[1]

        print(f"TCP server started on port {self.server_port}")
        while True:
            conn, _ = self.server_socket.accept()
            threading.Thread(target=handle_connection_callback, args=(conn,)).start()
    
    def send_file_in_chunks(self, conn, request_id, file_name):
        for i, chunk in enumerate(FileService.read_file_in_chunks(file_name), start=1):
            message = f"FILE {request_id} {file_name} {i} {chunk}"
            conn.sendall(message.encode('utf-8'))
        conn.sendall(f"FILE-END {request_id} {file_name} {i} ".encode('utf-8'))

    def receive_file_chunks(self, conn, output_file):
        data = ""
        while True:
            part = conn.recv(2048).decode('utf-8')
            if not part:
                break
            data += part
            while '\n' in data:  # Assuming messages are newline-terminated
                message, data = data.split('\n', 1)
                self.process_chunk(message, output_file)

    @staticmethod
    def process_chunk(message, output_file):
        parts = message.split(maxsplit=4)
        if parts[0] == "FILE-END":
            FileService.write_chunk_to_file(output_file, parts[4], mode='a')
            print(f"File {parts[2]} received successfully.")
            return False
        elif parts[0] == "FILE":
            FileService.write_chunk_to_file(output_file, parts[4], mode='a')
        return True