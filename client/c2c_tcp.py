import socket

class Client2ClientTCPCommunication:
    def receive_file(self, server_ip, server_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((server_ip, server_port))
            print(f"Connected to TCP server at {server_ip}:{server_port}")
            file_content = []
            while True:
                data = sock.recv(1024).decode('utf-8')
                if "FILE-END" in data:
                    _, chunk_number, text = data.split(maxsplit=2)
                    file_content.append((int(chunk_number), text))
                    break
                _, chunk_number, text = data.split(maxsplit=2)
                file_content.append((int(chunk_number), text))

            file_content.sort()
            with open('received_file.txt', 'w', encoding='utf-8') as f:
                for _, text in file_content:
                    f.write(text)
            print("File has been received and reassembled successfully.")

    def send_file(self, file_name, tcp_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('', tcp_port))
            server_socket.listen(1)
            print(f"TCP Server ready on port {tcp_port} for file {file_name}")
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            with open(file_name, 'rb') as f:
                while True:
                    bytes_read = f.read(1024)
                    if not bytes_read:
                        break
                    client_socket.sendall(bytes_read)
            client_socket.close()
            print("File has been sent successfully.")
