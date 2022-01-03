import sqlite3


def kreirajDatabaza():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    table_user = "CREATE TABLE IF NOT EXISTS user(username TEXT, password TEXT, email TEXT)"
    c.execute(table_user)

    table_poraka = "CREATE TABLE IF NOT EXISTS poraki(username TEXT, poraka TEXT)"
    c.execute(table_poraka)

    print("Uspesno ja kreiravte bazata!")

    conn.commit()
    conn.close()

kreirajDatabaza()