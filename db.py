import sqlite3
import datetime
from typing import List, Tuple


def init_db():
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()

    with open("create_db.sql", "r") as f:
        sql = f.read()
    cur.executescript(sql)
    conn.commit()

    cur.close()
    conn.close()


def add_message(message_id: int, message_text: str, send_date: datetime, user_id: int):
    try:
        conn = sqlite3.connect('bot.db')
        cur = conn.cursor()

        insert_message = """INSERT INTO message VALUES (?, ?, ?, ?);"""

        data = (message_id, message_text, send_date, user_id)
        cur.execute(insert_message, data)
        conn.commit()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if conn:
            conn.close()


def select_user() -> List[Tuple]:
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()

    cur.execute("""SELECT user_id FROM message""")
    records = cur.fetchall()

    cur.close()
    conn.close()

    return records


def get_users() -> List:
    return list(set([int(i[0]) for i in select_user()]))


def get_user_question(user_id):
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()

    cur.execute(
        """SELECT * FROM message WHERE user_id='{user_id}'""".format(
            user_id=user_id
        )
    )
    massages = cur.fetchall()

    cur.close()
    conn.close()

    return massages


def get_question(massage_id: int):
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()

    cur.execute(
        """SELECT * FROM message WHERE massage_id='{massage_id}'""".format(
            massage_id=massage_id
        )
    )
    massages = cur.fetchall()

    cur.close()
    conn.close()

    return massages[0]


def remove_question(massage_id: int):
    conn = sqlite3.connect('bot.db')
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM message WHERE massage_id='{massage_id}'".format(
            massage_id=massage_id
        )
    )
    conn.commit()

    cur.close()
    conn.close()
