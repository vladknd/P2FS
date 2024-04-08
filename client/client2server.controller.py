class Client2ServerController:
    def __init__(self, registration_service):
        self.registration_service = registration_service

    def register(self, name, ip, udp_port):
        self.registration_service.register(name, ip, udp_port)

    def deregister(self, name):
        self.registration_service.deregister(name)
