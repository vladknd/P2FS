import sys 
import socket
import threading
import time 
import sqlite3

from controller import Controller 
from request_handler import RequestHandler
from server_db import Database

class Server:
    def __init__(self, host='', port=3000):
        self.host = host
        self.port = port
        self.start_time = None
        self.current_time = None
        self.threads = []
        self.db = Database()
        self.clients = []

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.bind((self.host, self.port))
            self.request_handler = RequestHandler(self.db, self.server_socket)
        except socket.error as e:
            print('Failed to create/bind socket. Error Code : ' + str(e))
            sys.exit()
        print(f"Server listening on {self.host}:{self.port}")

    def start(self):
        self.db.load_data()
        self.start_time = time.time()

        update_thread = threading.Thread(target=self.update_handler)
        update_thread.daemon = True
        update_thread.start()

        self.threads.append(update_thread)
        try:
            while True:
                message, client_address = self.server_socket.recvfrom(4096)
                ip_address = client_address[0]
                port = client_address[1]
                message = message.decode()
                print(f"Received message from {client_address}: {message}")

                if message:
                    thread = threading.Thread(target=self.handle_request, args=((message, ip_address, port),))
                    thread.start()
                    self.threads.append(thread)
        except KeyboardInterrupt:
            print("Server shutting down.")
        finally:
            self.server_socket.close()

    def update_handler(self):
        while True:
            self.current_time = time.time()
            if self.current_time - self.start_time >= 300:
                self.start_time = time.time() # Reset the timer
                send_update = threading.Thread(target=self.send_update_message).start()

    def send_update_message(self):
        self.db = self.request_handler.server_db
        self.clients = self.db.get_clients()
        print(f"Current clients: {self.clients}")
        message = "UPDATE"
        clients_list = []
        for client in self.clients:
            name = client["name"]
            ip_address = client["ip"]
            port = int(client["udp_port"])
            files = self.db.get_files(client["name"])
            clients_list.append((name, ip_address, port, files))
        message = f"{message} {str(clients_list)}"
        print(f"Sending update message: {message}")
        for client in self.clients:
            ip_address = client["ip"]
            port = int(client["udp_port"])
            self.server_socket.sendto(message.encode(), (ip_address, port))
            print(f"Sent update message to {ip_address}:{port}")
        
    def handle_request(self, args):
        self.request_handler.server_db = self.db
        message, ip_address, port = args
        message_type, *rest = message.split()
        print(f"Received message from {ip_address}:{port}: {message}")
        print(message_type, args)
        if message_type == "REGISTER":
            resp = self.request_handler.register(args)
        elif message_type == "DE-REGISTER":
            resp = self.request_handler.deregister(args)
        elif message_type == "PUBLISH":
            resp = self.request_handler.publish(args)
        elif message_type == "REMOVE":
            resp = self.request_handler.remove(args)
        elif message_type == "UPDATE-CONTACT":
            resp = self.request_handler.update_contacts(args)
        else:
            print("Invalid message type")
            resp = "INVALID"
        print(f"Response: {resp}")
        if resp == "REGISTERED" or resp == "DE-REGISTERED" or resp == "PUBLISHED" or resp == "REMOVED":
            send_update = threading.Thread(target=self.send_update_message).start()

    def stop(self):
        self.server_socket.close()
        for thread in self.threads:
            thread.join()

            

