import socket
import sqlite3
import sys
import threading

ip =socket.gethostbyname(socket.gethostname())
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))

najaven = 0

def citajPoraki():
    while True:
        try:
            msg = client.recv(1024).decode("utf-8")
            print(msg)
        except:
            client.close()
            break

def pishuvajPoraki(username):
    while True:
        msg = input("")
        client.send(bytes(username + ": " + msg, "utf-8"))

        if msg == 'logout':
            client.close()
            sys.exit()

while True:
    komanda = input("Dobredojdovte vo Chat room.\nZa najava: login\n"
                    "Za odjavuvanje: logout\nZa registriranje: register\nZa da isklucite: exit\n")

    if komanda == "login":
        username = input("Vnesete username\n")
        password = input("Vnesete password\n")

        client.send(bytes("login|"+username+"|"+password, "utf-8"))
        porakaNajava = client.recv(1024).decode("utf-8")
        print(porakaNajava + "\n")

        if porakaNajava == "Se najavi " + username:
            najaven = 1
            break

    elif komanda == "register":
       username = input("Vnesete username\n")
       password = input("Vnesete password\n")
       email = input("Vnesete email\n")
       client.send(bytes("register|" + username + "|" + password + "|" + email, "utf-8"))
       print(client.recv(1024).decode("utf-8"))

    elif komanda == "exit":
        exit()
    else:
        print("Vnesovte pogresna komanda!!!\n")



if najaven == 1:
    threading.Thread(target=citajPoraki).start()
    threading.Thread(target=pishuvajPoraki, args=(username,)).start()






