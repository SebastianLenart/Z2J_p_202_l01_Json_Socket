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
SELECT_BASE_INFO = """select a.nick, a."password", a."admin"  from account a 
where nick = %s;"""
SELECT_NICKS_CONVERSATION = """SELECT
    CASE
        WHEN %s = c.id_receiver THEN (SELECT aa.nick FROM account aa WHERE aa.id_account = c.id_sender)
        WHEN %s = c.id_sender THEN (SELECT aa.nick FROM account aa WHERE aa.id_account = c.id_receiver)
    END AS return_value
FROM conversation c
WHERE %s IN (c.id_receiver, c.id_sender);"""
SELECT_ID_ACCOUNT_BY_NICK = """select id_account from account where nick = %s;"""
SELECT_COUNT_UNREAD_MESSAGES = """select a.nick, (select aa.nick as _from from
account aa
where aa.id_account = (select case 
	when cc.id_receiver = a.id_account then cc.id_sender
	else cc.id_receiver
end as return_value
from conversation cc 
where cc.id_conversation = c.id_conversation)), count(m.is_read is null) as unread_messages
from account a, conversation c 
inner join message m on m.id_conversation = c.id_conversation 
where (a.nick = %s and ((c.id_receiver = a.id_account and m.receiver_sender = 'send_to_receiver')
or (c.id_sender = a.id_account and m.receiver_sender = 'from_receiver')) and m.is_read = False)
group by a.nick, _from;"""
SELECT_UNREAD_MESSAGES = """select a.nick, c.id_conversation, m.id_message, (select aa.nick as _from from
account aa
where aa.id_account = (select case 
	when cc.id_receiver = a.id_account then cc.id_sender
	else cc.id_receiver
end as return_value
from conversation cc 
where cc.id_conversation = c.id_conversation)),
m."content" as unread_message
from account a, conversation c 
inner join message m on m.id_conversation = c.id_conversation 
where (a.nick = %s and ((c.id_receiver = a.id_account and m.receiver_sender = 'send_to_receiver')
or (c.id_sender = a.id_account and m.receiver_sender = 'from_receiver')) and m.is_read = FALSE)
order by c.id_conversation, m."time" ;"""
INSERT_NEW_USER = """INSERT INTO account (nick, password, admin) 
VALUES (%s, %s, %s) RETURNING id_account;"""
UPDATE_UNREAD_MESSAGES = """update message 
set is_read = True
where id_message = %s;"""


def change_sth_test(connetion):
    with connetion.get_cursor() as cursor:
        cursor.execute("""update message
    set content = 'He Ol'
    where id_message = 1;""")


def get_list_nicks(connection):
    with connection.get_cursor() as cursor:
        cursor.execute(SELECT_LIST_USERS)
        return cursor.fetchall()


def get_base_info(connection, nick):
    with connection.get_cursor() as cursor:
        cursor.execute(SELECT_BASE_INFO, (nick,))
        return cursor.fetchone()


def add_new_user(connection, nick, password, admin):
    with connection.get_cursor() as cursor:
        cursor.execute(INSERT_NEW_USER, (nick, password, admin))
        return cursor.fetchall()[0]


def get_nicks_conversation(connection, nick="Seba"):
    with connection.get_cursor() as cursor:
        cursor.execute(SELECT_ID_ACCOUNT_BY_NICK, (nick,))
        try:
            idd = cursor.fetchone()[0]
            cursor.execute(SELECT_NICKS_CONVERSATION, (idd, idd, idd))
        except TypeError:
            return []
        return cursor.fetchall()


def get_counter_unread_messages(connection, nick="Seba"):
    with connection.get_cursor() as cursor:
        cursor.execute(SELECT_COUNT_UNREAD_MESSAGES, (nick,))
        return cursor.fetchall()


def get_unread_messages(connection, nick="Seba"):
    with connection.get_cursor() as cursor:
        cursor.execute(SELECT_UNREAD_MESSAGES, (nick,))
        return cursor.fetchall()


def update_unread_message(connection, id_message):
    with connection.get_cursor() as cursor:
        cursor.execute(UPDATE_UNREAD_MESSAGES, (id_message,))

