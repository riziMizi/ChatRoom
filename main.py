import sqlite3
import socket

class korisnik():
    def __init__(self, username, password, adresa):
        self.username, self.password, self.adresa = username, password, adresa

ip =socket.gethostbyname(socket.gethostname())
port = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen(20)

conn = sqlite3.connect('users.db')
c = conn.cursor()

while True:
    korisnici = {}
    client, addr = server.accept()

    data =client.recv(1024).decode("utf-8")
    poraka = data.split("|")
    tip = poraka[0]

    if tip == "login":
        username = poraka[1]
        password = poraka[2]
        c.execute("SELECT * FROM user WHERE username = '" + username + "' AND password = '" + password + "'")
        item = c.fetchone()

        if item == None:
            client.send(bytes("Pogresen username ili password.Obidete se povtorno!", "utf-8"))
        else:
            korisnici[username] = korisnik(username, password, client)
            print("Se najavi " + username)
            client.send(bytes("Uspesno se najavivte!", "utf-8"))
    elif tip == "send":
        if poraka[1] == "logout":
            exit()
        else:
            print(poraka[1])



conn.commit()
conn.close()
