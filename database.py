import sqlite3


def kreirajDatabaza():
    conn = sqlite3.connect("chatroom.db")
    c = conn.cursor()

    table_user = "CREATE TABLE IF NOT EXISTS user(username TEXT, password TEXT, email TEXT)"
    c.execute(table_user)

    table_poraka = "CREATE TABLE IF NOT EXISTS poraki(username TEXT, poraka TEXT)"
    c.execute(table_poraka)

    print("You have successfully created the database!")

    conn.commit()
    conn.close()

kreirajDatabaza()