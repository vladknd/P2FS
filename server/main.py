import socket
from server import Server


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    port = s.getsockname()[1]
    s.close()
    print(host, port)
    # server = Server(host=str(host), port=int(port))
    server = Server(host=host, port=3000)

    # server = UDPServer(host='localhost', port=80)

    server.start()

if __name__ == "__main__":
    main()