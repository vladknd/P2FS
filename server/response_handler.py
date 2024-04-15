import threading 

class ResponseHandler: 
    def __init__(self, server):
        self.server = server

    def register_response(self, args):
        client_address, response = args
        self.server.server_socket.sendto(response.encode(), client_address)
        print(f"Sent response to {client_address}")
        
        