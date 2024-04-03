class Controller:
    # Class variable to hold the command handler registry
    router = None

    @classmethod
    def set_router(cls, router):
        """
        Sets the router for the Controller.
        
        :param router: An instance of Router.
        """
        cls.router = router

    @staticmethod
    def parse_message(message):
        """
        Parses the incoming message and extracts the command and data.
        
        :param message: The incoming message as a bytes object.
        :return: A tuple containing the command and a list of data parts.
        """
        parts = message.decode().split()
        command = parts[0]
        data = parts[1:]
        return command, data

    @classmethod
    def route(cls, message, address, server_socket):
        """
        Routes the incoming message to the appropriate command handler.
        
        :param message: The incoming message as a bytes object.
        :param address: The address of the client that sent the message.
        :param server_socket: The server socket through which responses can be sent.
        """
        command, data = cls.parse_message(message)
        handler_class = cls.router.get_handler(command)
        if handler_class:
            handler = handler_class()
            handler.handle(data, address, server_socket)
        else:
            print(f"No handler found for command: {command}")
