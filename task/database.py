from pprint import pprint

CREATE_ACCOUNT = """CREATE TABLE IF NOT EXISTS account 
(id_account SERIAL PRIMARY KEY, nick TEXT, password TEXT, admin BOOLEAN);"""

CREATE_CONVERSATION = """CREATE TABLE IF NOT EXISTS conversation
(id_conversation SERIAL PRIMARY KEY, id_receiver INTEGER, id_sender INTEGER,
FOREIGN KEY(id_sender) REFERENCES account (id_account),
FOREIGN KEY(id_receiver) REFERENCES account (id_account));"""

CREATE_MESSAGE = """CREATE TABLE IF NOT EXISTS message
(id_message SERIAL PRIMARY KEY, receiver_sender TEXT, content TEXT, time TEXT, is_read BOOLEAN,
id_conversation INTEGER, FOREIGN KEY(id_conversation) REFERENCES conversation (id_conversation));"""

SELECT_LIST_USERS = """select nick from account;"""
INSERT_NEW_USER = """INSERT INTO account (nick, password, admin) 
VALUES (%s, %s, %s) RETURNING id_account;"""


def change_sth_test(connetion):
    with connetion.get_cursor() as cursor:
        cursor.execute("""update message
    set content = 'He Ol'
    where id_message = 1;""")


def get_list_nicks(connection):
    with connection.get_cursor() as cursor:
        cursor.execute(SELECT_LIST_USERS)
        return cursor.fetchall()


def add_new_user(connection, nick, password, admin):
    with connection.get_cursor() as cursor:
        cursor.execute(INSERT_NEW_USER, (nick, password, admin))
        return cursor.fetchall()[0]