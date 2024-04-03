class Router:
    def __init__(self):
        self.handlers = {}

    def register_handler(self, command, handler):
        self.handlers[command] = handler

    def get_handler(self, command):
        return self.handlers.get(command, None)
