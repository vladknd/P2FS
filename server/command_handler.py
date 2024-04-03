class CommandHandler:
    def handle(self, data, client_address, server_socket):
        raise NotImplementedError

class RegisterCommandHandler(CommandHandler):
    def handle(self, data, client_address, server_socket):
        print(f"Handling REGISTER command from {client_address}, data: {data}")
        response_message = "REGISTERED"
        server_socket.sendto(response_message.encode(), client_address)

class PublishCommandHandler(CommandHandler):
    def handle(self, data, client_address, server_socket):
        print(f"Handling PUBLISH command from {client_address}, data: {data}")
        response_message = "PUBLISHED"
        server_socket.sendto(response_message.encode(), client_address)

