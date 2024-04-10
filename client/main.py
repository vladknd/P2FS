from c2c_controller import Client2ClientController

def main():
    udp_bind_port = 3006  # Example UDP port
    controller = Client2ClientController(udp_bind_port)
    controller.start_udp_server()

    # Example of requesting a file from a peer (to be filled based on your application logic)
    # controller.request_file(peer_ip='localhost', peer_port=3005, request_id='1', file_name='text.txt')

if __name__ == "__main__":
    main()
