import sqlite3  # Import SQLite3 module for database operations
import hashlib  # Import hashlib module for hashing functions

def hash_password(password):
    # Convert the password to bytes
    password_bytes = password.encode('utf-8')

    # Use SHA-256 hash function
    hashed_bytes = hashlib.sha256(password_bytes).digest()

    # Convert the hashed bytes to a hex string
    hashed_password = hashed_bytes.hex()

    return hashed_password
def update_location(user_id, location):
    cursor, connection = connect()

    # Fetch the location corresponding to the given alert_id from the alerts table
    cursor.execute("SELECT location FROM alerts WHERE user_id=?", (user_id,))
    row = cursor.fetchone()

    if row:
        
        # Update the location column in the user_data table for the user associated with the alert
        cursor.execute("UPDATE alerts SET location=? WHERE user_id=?", (location, user_id))
        connection.commit()
        print("Location updated successfully.")
    else:
        print("Alert ID not found.")

    connection.close()



def connect():
    # Establish connection to the SQLite database named "cs_project.db"
    connection = sqlite3.connect("cs_project.db")

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    return cursor, connection 

def sign_up_log(email, password, user_name, VIN, first_name):
    # Hash the password
    hashed_password = hash_password(password)
    
    # Establish connection to the database
    cursor, connection = connect()
    
    # Execute an SQL command to insert user data into the database
    cursor.execute('''INSERT INTO user_data (email_address, pass_has, username, VIN_no, first_name)
                  VALUES (?, ?, ?, ?, ?)''', 
                  (email, hashed_password, user_name, VIN, first_name))
    cursor.execute("SELECT * FROM user_data")
    rows = cursor.fetchall()
    print(rows)
    # Commit the transaction
    connection.commit()
    
    # Close the connection
    connection.close()

def login_check(username, password):
    # Hash the password for comparison
    hashed_password = hash_password(password)
    
    # Establish connection to the database
    cursor, connection = connect()
    
    # Execute an SQL command to retrieve hashed password for the given username
    cursor.execute("SELECT pass_has FROM user_data WHERE username=?", (username,))
    
    rows = cursor.fetchall()
    
    #print(rows)
    # If no matching username is found, return False
    if len(rows) == 0:
        print('failed')
        return False, None
    # If the hashed password matches, return True
    elif hashed_password == rows[0][0]:
        print(hashed_password, rows[0][0])
        print('worked')
        cursor.execute("SELECT user_id FROM user_data WHERE username=?", (username,))
        rows = cursor.fetchall()
        #print(rows[0][0])
        connection.commit()
        connection.close()
        return True, rows[0][0]
    # If passwords do not match, return False
    else:
        print('failed')
        return False, None

def alert_log(g, a, r, reason, location, user_id):
    # Establish connection to the database
    cursor, connection = connect()
    
    # Execute an SQL command to insert alert data into the database
    cursor.execute('''INSERT INTO alerts (red, amber, green , reason, location, user_id)
                  VALUES (?, ?, ?, ?, ?, ?)''', 
                  (g,a,r, reason, location, user_id))
    cursor.execute("SELECT * FROM alerts")
    rows = cursor.fetchall()
    print(rows)
    
    # Commit the transaction
    connection.commit()
    
    # Close the connection
    connection.close()
    
    
#cursor.execute("SELECT * FROM alerts WHERE user_id=12")    rows = cursor.fetchall()
#print(rows)



#alert_log(0,1,0, 'Stolen car', 'bing bong', 12)



#sign_up_log('tomkenison765@gmail.com', 'Ashcat123!', 'tom2865476848938', '2865476848938', 'tom')


#login_check('tom2865476848938','Ashcat123!')
#username='tom2865476848938'
cursor, connection = connect()
#cursor.execute(f"DELETE FROM alerts")
#cursor.execute(f"SELECT * FROM user_data")
#rows = cursor.fetchall()
#print(rows)
#cursor.execute("SELECT pass_has FROM user_data WHERE username=?", (username,))
#rows = cursor.fetchall()
#print(rows)
connection.commit()
connection.close()




#for row in rows:
#    print(row)
#connection.close()



#import argon2
 
# Declare the password as a bytes object
#password = b'MySecurePassword'
 
# Hash the password using Argon2
#hashed_password = argon2.hash_password(password)
 
# Print the hashed password#
#print(hashed_password)







                            