import sqlite3
import socket
import threading
import re
from mail import sendEmail


ip =socket.gethostbyname(socket.gethostname())
port = 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen(20)

korisnici = {}

def addUser(username, password, email):
    conn = sqlite3.connect('chatroom.db')
    c = conn.cursor()

    sql = "INSERT INTO user (username, password, email) VALUES (?, ?, ?);"
    user = (username, password, email)
    c.execute(sql, user)

    conn.commit()
    conn.close()

def getUser(username, password):
    conn = sqlite3.connect('chatroom.db')
    c = conn.cursor()

    sql = "SELECT * FROM user WHERE username = ? AND password = ?"
    c.execute(sql, (username, password,))
    item = c.fetchone()

    conn.commit()
    conn.close()

    return item

def checkUsername(username):
    conn = sqlite3.connect('chatroom.db')
    c = conn.cursor()

    sql = "SELECT * FROM user WHERE username = ?"
    c.execute(sql, (username,))
    item = c.fetchone()

    conn.commit()
    conn.close()

    return item

def addMessage(username, msg):
    conn = sqlite3.connect('chatroom.db')
    c = conn.cursor()

    sql = "INSERT INTO poraki (username, poraka) VALUES (?, ?);"
    poraka = (username, msg)
    c.execute(sql, poraka)

    conn.commit()
    conn.close()


def checkEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if (re.fullmatch(regex, email)):
        return True
    else:
        return False

def broadcast(msg):
    for korisnik in korisnici.values():
        korisnik.send(bytes(msg, "utf-8"))

def opsluzhiKorisnik(client):
    while True:
        data = client.recv(1024).decode("utf-8")
        poraka = data.split("|")
        tip = poraka[0]

        if tip == "login":
            username = poraka[1]
            if username in korisnici:
                client.send(bytes("You are already logged in to the server!\n", "utf-8"))
            else:
                password = poraka[2]
                item = getUser(username, password)
                if item == None:
                    client.send(bytes("Wrong username or password. Please try again!\n", "utf-8"))
                else:
                    korisnici[username] = client
                    broadcast(f"{username} is now online!")
                    print(f"{username} is now online!\n")
                    ispratiSitePoraki(client)

        elif tip == "register":
            username = poraka[1]
            password = poraka[2]
            email = poraka[3]
            item = checkUsername(username)

            if item == None:
                if checkEmail(email):
                    addUser(username, password, email)
                    client.send(bytes("You have successfully registered in Chat Room!!\n", "utf-8"))
                    sendEmail(email, "Registering in Chat Room!", f"Hello {username}. You have successfully registered in Chat Room!")
                else:
                    client.send(bytes("You entered an invalid email address. Please try again!\n", "utf-8"))
            else:
                client.send(bytes(f"Username {username} is already taken!\n", "utf-8"))


        elif tip == "send":
            try:
                proverkaOdjava = poraka[1].split(":")
                if proverkaOdjava[1].strip() == 'logout':
                    user = list(korisnici.keys())[list(korisnici.values()).index(client)]
                    del korisnici[user]
                    client.close()
                    odjava = f"{user} is now offline!"
                    print(odjava)
                    broadcast(odjava)
                    break

                broadcast(poraka[1])
                addMessage(proverkaOdjava[0], proverkaOdjava[1])
            except:
                user = list(korisnici.keys())[list(korisnici.values()).index(client)]
                del korisnici[user]
                client.close()
                break


def ispratiSitePoraki(client):
    conn = sqlite3.connect('chatroom.db')
    c = conn.cursor()

    sql = "SELECT * FROM poraki"
    c.execute(sql)
    item = c.fetchall()
    for i in item:
        client.send(bytes(f"{i[0]}: {i[1].strip()}\n", "utf-8"))

    conn.commit()
    conn.close()
    return item

def main():
    while True:
        client, addr = server.accept()
        threading.Thread(target=opsluzhiKorisnik, args=(client,)).start()


main()

