#Global imports
import socket

#Local imports
from controller import Controller
from server import UDPServer
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
    server = UDPServer(host='localhost', port=80)
    server.start()

if __name__ == "__main__":
    main()