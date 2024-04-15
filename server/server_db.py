import json
import os

class Database:
    def __init__(self):
        self.clients_file = 'clients.json'
        self.files_file = 'files.json'
        self.clients_data = []
        self.files_data = []
        self.load_data()

    def load_data(self):
        # Initialize data dictionaries or create files if they don't exist
        if not os.path.exists(self.clients_file):
            with open(self.clients_file, 'w') as clients_file:
                json.dump([], clients_file)
        if not os.path.exists(self.files_file):
            with open(self.files_file, 'w') as files_file:
                json.dump([], files_file)
        
        # Load data from JSON files
        with open(self.clients_file, 'r') as clients_file:
            self.clients_data = json.load(clients_file)
        with open(self.files_file, 'r') as files_file:
            self.files_data = json.load(files_file)

    def insert_client(self, name, ip, udp_port):
        client_id = len(self.clients_data) + 1
        self.clients_data.append({'id': client_id, 'name': name, 'ip': ip, 'udp_port': udp_port})
        self.save_data()

    def insert_files(self, name, files):
        self.files_data.append({'client_name': name, 'files': files})
        self.save_data()

    def delete_client(self, name):
        self.clients_data = [client for client in self.clients_data if client['name'] != name]
        self.files_data = [file for file in self.files_data if file['client_name'] != name]
        self.save_data()

    def delete_files(self, name, files):
        for file in self.files_data:
            print(file)
            if file['client_name'] == name:
                file['files'] = [f for f in file['files'] if f not in files]
                print(f"Deleted files: {files}")
        self.save_data()
        

    def check_client(self, name, ip=None):
        if ip is None:
            return any(client['name'] == name for client in self.clients_data)
        return any(client['name'] == name or client['ip'] == ip for client in self.clients_data)

    def save_data(self):
        # Save data to JSON files
        with open(self.clients_file, 'w') as clients_file:
            json.dump(self.clients_data, clients_file, indent=4)
        with open(self.files_file, 'w') as files_file:
            json.dump(self.files_data, files_file, indent=4)

    def get_client(self, name):
        for client in self.clients_data:
            if client['name'] == name:
                return client['ip'], client['udp_port']
        return None, None

    def get_clients(self):
        return self.clients_data
    
    def get_files(self, name):
        for file in self.files_data:
            if file['client_name'] == name:
                return file['files']
        return []
    
    def close(self):
        pass  # JSON files do not require explicit closing
