import sqlite3

conn = sqlite3.connect('client_data.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        ip TEXT NOT NULL,
        udp_port INTEGER NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS files (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL,
        client_id INTEGER,
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
''')

# Insert sample data into the tables (replace with your actual data)
client_data = [
    ('Alice', '192.168.1.100', 5000),
    ('Bob', '192.168.1.101', 5001)
]

file_data = [
    ('file1.txt', 1),  # File 'file1.txt' published by client with id 1 (Alice)
    ('file2.txt', 2)   # File 'file2.txt' published by client with id 2 (Bob)
]

cursor.executemany('INSERT INTO clients (name, ip, udp_port) VALUES (?, ?, ?)', client_data)
cursor.executemany('INSERT INTO files (filename, client_id) VALUES (?, ?)', file_data)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Data stored successfully.")
