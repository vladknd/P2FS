class RegistrationService:
    def __init__(self, udp_communication_service, server_ip, server_port):
        self.udp_communication_service = udp_communication_service
        self.server_address = (server_ip, server_port)

    def register(self, name, ip, udp_port):
        message = f"REGISTER RQ# {name} {ip} {udp_port}"
        self.udp_communication_service.send_message(message, self.server_address)
        # Listen for server response and handle accordingly.

    def deregister(self, name):
        message = f"DE-REGISTER RQ# {name}"
        self.udp_communication_service.send_message(message, self.server_address)
        # Optionally listen for server confirmation or error.