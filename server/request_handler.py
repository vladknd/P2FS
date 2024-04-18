import threading
import time

class RequestHandler: 
    def __init__(self, server_db, server_socket):
        self.server_db = server_db
        self.server_socket = server_socket
        self.threads = []

    def register(self, args):
        message, *client_address = args
        message_type, request_number, name, ip_address, udp_port = message.split()
        if not self.server_db.check_client(name, ip_address): 
            self.server_db.insert_client(name, ip_address, udp_port)
            response = "REGISTERED"
            response_message = f"{response} {request_number}"
        else: 
            response = "REGISTER-DENIED"
            reason = "Client already registered."
            response_message = f"{response} {request_number} {reason}"
        thread = threading.Thread(target=self.send_response, args=((response_message, client_address),)).start()
        self.threads.append(thread)
        return response

    def deregister(self, args):
        message, *client_address = args
        message_type, request_number, name = message.split()
        response = "INVALID"

        if self.server_db.check_client(name):
            self.server_db.delete_client(name)
            response = "DE-REGISTERED"
        return response

    def publish(self, args):
        print(args)
        message, *client_address = args
        message_type, request_number, name, *files = message.split()
        files = [file.strip("[''],") for file in files]
        if self.server_db.check_client(name):
            self.server_db.insert_files(name, files)
            response = "PUBLISHED"
            response_message = f"{response} {request_number}"
        else:
            response = "PUBLISH-DENIED"
            reason = "Client name not registered."
            response_message = f"{response} {request_number} {reason}"
        thread = threading.Thread(target=self.send_response, args=((response_message, client_address),)).start()
        self.threads.append(thread)
        return response
    
    def remove(self, args):
        message, *client_address = args
        message_type, request_number, name, *files = message.split()
        files = [file.strip("[''],") for file in files]
        if self.server_db.check_client(name):
            self.server_db.delete_files(name, files)
            response = "REMOVED"
            response_message = f"{response} {request_number}"
        else:
            response = "REMOVE-DENIED"
            reason = "Client name not registered."
            response_message = f"{response} {request_number} {reason}"
        thread = threading.Thread(target=self.send_response, args=((response_message, client_address),)).start()
        self.threads.append(thread)
        return response
    
    def update_contacts(self, args):
        message, *client_address = args
        message_type, request_number, name, ip_address, udp_port = message.split()
        if self.server_db.check_client(name):
            self.server_db.update_client(name, ip_address, udp_port)
            response = "UPDATE-CONFIRMED"
            response_message = f"{response} {request_number} {name} {ip_address} {udp_port}"
            client_address = (ip_address, udp_port)
        else:
            response = "UPDATE-DENIED"
            reason = "Client name not registered."
            response_message = f"{response} {request_number} {reason}"
        thread = threading.Thread(target=self.send_response, args=((response_message, client_address),)).start()
        self.threads.append(thread)
        return response

    def send_response(self, args):
        response, *client_address = args
        client_address = client_address[0]
        self.server_socket.sendto(response.encode(), (client_address[0], int(client_address[1])))

        
        