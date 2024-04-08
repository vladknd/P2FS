import sqlite3 as sq


# creating the database or connecting to the already existing one 
con = sq.connect("database_test.db")
cur = con.cursor()

#creating the table if not already created


# ----------------------------------------------------------------------------------------------------------#

# creatng the table clients if it does not exist and doing nothing if it does

# Check if the 'users' table exists
cur.execute("SELECT name FROM sqlite_master WHERE name='users' ")

# Fetch the result
table_exists = cur.fetchone()

# If the 'users' table doesn't exist, create it
if table_exists is None:
    cur.execute('''CREATE TABLE users (
                    id INTEGER PRIMARY KEY,
                    how_to_reach TEXT NOT NULL,
                    )''')
    con.commit()
    print("Table 'users' created successfully.")


# Close the connection
con.close()
# ----------------------------------------------------------------------------------------------------------#




# creating the table for storing the list of files and what user owns the file

# ----------------------------------------------------------------------------------------------------------#


# creating the connection
con = sq.connect("database_test.db")
cur = con.cursor()


# creatng the table clients if it does not exist and doing nothing if it does

# Check if the 'files' table exists
cur.execute("SELECT name FROM sqlite_master WHERE name='files' ")

# Fetch the result
table_exists = cur.fetchone()

# If the 'files' table doesn't exist, create it
if table_exists is None:
    cur.execute('''CREATE TABLE files (
                    id INTEGER,
                    file TEXT NOT NULL,
                    )''')
    con.commit()
    print("Table 'files' created successfully.")


# Close the connection
con.close()
# ----------------------------------------------------------------------------------------------------------#



# Functions used to interact with the databases 


# ----------------------------------------------------------------------------------------------------------#

def insert_user(username, how_to_reach):
    # creating the connection
    con = sq.connect("database_test.db")
    cur = con.cursor()

    """
    Insert a new user into the 'users' table.
    """

    cur.execute("INSERT INTO users (id, how_to_reach) VALUES (?, ?)", (username, how_to_reach))
    con.commit()
    # Close the connection
    con.close()


def insert_file(id, file):
    # creating the connection
    con = sq.connect("database_test.db")
    cur = con.cursor()

    """
    Insert a new user into the 'users' table.
    """
    cur.execute("INSERT INTO users (id, file) VALUES (?, ?)", (id, file))
    con.commit()
    # Close the connection
    con.close()


def fetch_all_users():
    # creating the connection
    con = sq.connect("database_test.db")
    cur = con.cursor()

    """
    Fetch all users from the 'users' table.
    """
    cur.execute("SELECT * FROM users")
    users  = cur.fetchall()
    # Close the connection
    con.close()
    return users


def fetch_user_conn_info(user):
    # creating the connection
    con = sq.connect("database_test.db")
    cur = con.cursor()

    """
    Fetch the information on how to reach a user.
    """
    cur.execute("SELECT how_to_reach FROM users WHERE id = ?",(user))
    info  = cur.fetchall()
    # Close the connection
    con.close()
    return info


def fetch_file_table(user):
  
    # creating the connection
    con = sq.connect("database_test.db")
    cur = con.cursor()

    """
    getting all the files that a certain user has
    """
    cur.execute("SELECT file FROM files WHERE id = ?",(user))
    info  = cur.fetchall()
    # Close the connection
    con.close()
    return info

# ----------------------------------------------------------------------------------------------------------#