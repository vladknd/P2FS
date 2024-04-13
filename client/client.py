class Client:
    def __init__(self, name, host, port, udp_port):
        self.name = name
        self.host = host
        self.port = port
        self.udp_port = udp_port

    def start(self):
        pass

    def send_message(self, message):
        pass

    def receive_message(self):
        pass


