import socket
import sys

from controller import Controller
from server import Server
from router import Router

#Command handler imports
from command_handler import RegisterCommandHandler, PublishCommandHandler

def setup():
    """
    Sets up the Router and Controller and registers command handlers.
    """

    # Router setup
    router = Router()
    router.register_handler("REGISTER", RegisterCommandHandler)
    router.register_handler("PUBLISH", PublishCommandHandler)

    # Controller setup
    Controller.set_router(router)

def main():
    setup()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    port = s.getsockname()[1]
    s.close()
    server = Server(host=str(host), port=int(port))
    server.start()

if __name__ == "__main__":
    main()