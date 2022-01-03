import socket
import sys
import threading

ip =socket.gethostbyname(socket.gethostname())
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))

najaven = 0
username = ""

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
        client.send(bytes("send|" + username + ": " + msg, "utf-8"))

        if msg == 'logout':
            client.close()
            sys.exit()

def main():
    while True:
        global username
        global najaven

        komanda = input("Welcome to Chat Room.\nFor logging in: login\n"
                        "For logging out: logout\nFor registration: register\nExit: exit\n")

        if komanda == "login":
            username = input("Enter username:\n")
            password = input("Enter password:\n")

            client.send(bytes("login|" + username + "|" + password, "utf-8"))
            porakaNajava = client.recv(1024).decode("utf-8")
            print(porakaNajava + "\n")

            if porakaNajava == f"{username} is now online!":
                print(f"Welcome {username} in Chat Room!\n")
                najaven = 1
                break

        elif komanda == "register":
           username = input("Enter username:\n")
           password = input("Enter password:\n")
           email = input("Enter email:\n")
           client.send(bytes("register|" + username + "|" + password + "|" + email, "utf-8"))
           print(client.recv(1024).decode("utf-8"))

        elif komanda == "exit":
            exit()
        else:
            print("Invalid command!!!\n")


main()
if najaven == 1:
    threading.Thread(target=citajPoraki).start()
    threading.Thread(target=pishuvajPoraki, args=(username,)).start()






