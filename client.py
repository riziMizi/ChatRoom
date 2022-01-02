import socket

ip =socket.gethostbyname(socket.gethostname())
port = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, port))

najaven = 0

while True:
    komanda = input("Dobredojdovte vo Chat room.\nZa najava: login\n"
                    "Za registriranje: register\nZa odjavuvanje: logout\n")
    if komanda == "login":
        username = input("Vnesete username\n")
        password = input("Vnesete password\n")
        client.send(bytes("login|"+username+"|"+password, "utf-8"))
        porakaNajava = client.recv(1024).decode("utf-8")
        print(porakaNajava + "\n")
        if porakaNajava == "Uspesno se najavivte!":
            najaven = 1
            break
    elif komanda == "register":
        print("register")

    elif komanda == "logout":
        exit()
    else:
        print("Pogresna komanda\n")

if najaven == 1:
    while True:
        poraka = input("Prati poraka:\n")
        client.send(bytes("send|"+poraka, "utf-8"))
        if poraka == "logout":
            exit()






