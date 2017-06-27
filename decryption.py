import os
import sys
import sqlite3
from windows_cryptography import decrypt


if os.name != "nt":
    sys.exit("ERROR: Must be using a Windows machine")

# Get file location of the 'Login Data' sql file that contains saved passwords.
folder = os.getenv("LOCALAPPDATA") + r"\Google\Chrome\User Data\Default"
if not os.path.isdir(folder):
    sys.exit("ERROR: Could not find Chrome path.")

# Open the SQLite3 data file.
try:
    connection = sqlite3.connect(folder + "\Login Data")
    c = connection.cursor()
    # Blacklisted_by_user = 0 will filter out the sites where passwords are never remembered.
    c.execute('SELECT action_url, username_value, password_value FROM logins WHERE blacklisted_by_user = 0')
    query_results = c.fetchall()

# Make the error messages easier to understand.
except sqlite3.OperationalError as error_code:
    error_code = str(error_code)
    if error_code == "database is locked":
        sys.exit("Error: File is in use by Chrome. Close all instances of Chrome and retry.")
    elif error_code == "no such table: logins":
        sys.exit("Error: Password storage file was not found.")
    else:
        sys.exit(error_code)

results = ""
for entry in query_results:
    password_data = decrypt(entry[2])
    if password_data:
        # Remove the LMEM garbage from the end of the password. password_data[1] is the length of the password.
        password = password_data[0][:password_data[1]]
        # Convert from bytes to unicode string.
        password = password.decode("UTF-8")
        results += "Website: %s\nUsername: %s\nPassword: %s\n\n" % (entry[0], entry[1], password)

print(results)
