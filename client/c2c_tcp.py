import socket
import threading

class Client2ClientTCPCommunication:
    def __init__(self):
        self.rq = 0
        # self.lock = threading.Lock()

    def receive_file(self, server_ip, server_port):
        print(f"Running in thread: {threading.current_thread().name}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # Connect to the specified IP and port
            sock.connect((server_ip, server_port))
            print(f"Connected to TCP server at {server_ip}:{server_port}")

            # self.lock.acquire()
            file_content = []
            file_name = None  # Variable to store the file name once it's retrieved
            while True:
                data = sock.recv(200).decode('utf-8')
                print(f"Received DATA:>>> {data}")
                # Check if this is the last chunk
                if "FILE-END" in data:
                    prefix, rq, file_name, chunk_number, text = data.split(maxsplit=4)
                    print(f"ALl we got from data split is {prefix} - {rq} - {file_name} - {chunk_number} - {text} >>>>>")
                    print(f"RECEIVING CHUNK #: {chunk_number} - {text} END OF TEXT")
                    file_content.append((int(chunk_number), text))
                    break  # Exit the loop since it's the last chunk
                else:
                    prefix, rq, file_name, chunk_number, text = data.split(maxsplit=4)
                    print(f"ALl we got from data split is {prefix} - {rq} - {file_name} - {chunk_number} - {text}>>>>>")
                    print(f"RECEIVING CHUNK #: {chunk_number} - {text} END OF TEXT")
                    file_content.append((int(chunk_number), text))

            # self.lock.release()
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
        print(f"Running in thread: {threading.current_thread().name}")
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
                        header = f"FILE {self.rq} {file_name} {chunk_number} "
                        header_length = len(header)
                        body_size = 200 - header_length
                        bytes_read = f.read(body_size)
                        message_size = header_length + bytes_read.__sizeof__()
                        print(f"Sizes are HEADER>>{header_length}  BODY>>{body_size} - MSG>>{message_size} - FILE>>{bytes_read}")

                        if not bytes_read:
                            # No more bytes are read from the file
                            break
                        if message_size < 200:
                            # This is the last chunk as it contains less than 200 bytes
                            print(f"SENDING CHUNK #: {chunk_number} - {bytes_read.decode()}")
                            message = f"FILE-END {self.rq} {file_name} {chunk_number} {bytes_read.decode()}"
                            print(f"END message to be sent is {message}")
                        else:
                            # Format the message for a regular chunk
                            print(f"SENDING CHUNK #: {chunk_number} - {bytes_read.decode()}")
                            message = f"FILE RQ# {file_name} {chunk_number} {bytes_read.decode()}"
                            print(f"message to be sent is {message}")
                        
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