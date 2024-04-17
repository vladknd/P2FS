import socket

class Client2ClientTCPCommunication:
    def receive_file(self, server_ip, server_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to the specified IP and port
            sock.connect((server_ip, server_port))
            print(f"Connected to TCP server at {server_ip}:{server_port}")

            file_content = []
            file_name = None  # Variable to store the file name once it's retrieved
            while True:
                # Receive data in blocks of 1024 bytes
                data = sock.recv(1024).decode('utf-8')
                
                # Check if this is the last chunk
                if "FILE-END" in data:
                    prefix, rq, file_name, chunk_number, text = data.split(maxsplit=4)
                    print(f"ALl we got from data split is {prefix} - {rq} - {file_name} - {chunk_number} - {text}")
                    file_content.append((int(chunk_number), text))
                    break  # Exit the loop since it's the last chunk
                else:
                    prefix, file_name, chunk_number, text = data.split(maxsplit=3)
                    file_content.append((int(chunk_number), text))

            # Sort the file content by chunk number (tuple first element)
            file_content.sort()
            
            # Save the file using the extracted file name
            if file_name is not None:
                with open(f'{file_name}', 'w', encoding='utf-8') as f:
                    for _, text in file_content:
                        f.write(text)
                print(f"File {file_name} has been received and reassembled successfully.")
            else:
                print("Error: File name could not be determined.")

    def send_file(self, file_name, tcp_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Bind the socket to all available IPs and the specified TCP port
            server_socket.bind(('', tcp_port))
            # Start listening for incoming connections; only allow 1 connection
            server_socket.listen(1)
            print(f"TCP Server ready on port {tcp_port} for file {file_name}")
            
            # Accept a connection from a client
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            
            try:
                chunk_number = 1  # Initialize chunk number
                # Open the file in binary read mode
                with open(f'./files/{file_name}.txt', 'rb') as f:
                    while True:
                        # Read up to 200 bytes from the file
                        bytes_read = f.read(200)
                        if not bytes_read:
                            # No more bytes are read from the file
                            break
                        if len(bytes_read) < 200:
                            # This is the last chunk as it contains less than 200 bytes
                            message = f"FILE-END RQ# {file_name} {chunk_number} {bytes_read.decode()}"
                        else:
                            # Format the message for a regular chunk
                            message = f"FILE RQ# {file_name} {chunk_number} {bytes_read.decode()}"
                        
                        # Send the formatted message
                        client_socket.sendall(message.encode())
                        chunk_number += 1  # Increment the chunk number

                print("File has been sent successfully.")
            finally:
                # Close the client socket
                client_socket.close()

    def find_free_port(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            return s.getsockname()[1]