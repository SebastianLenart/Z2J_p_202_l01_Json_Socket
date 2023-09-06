

CREATE_ACCOUNT = """CREATE TABLE IF NOT EXISTS account 
(id_account SERIAL PRIMARY KEY, nick TEXT, password TEXT, admin BOOLEAN);"""

CREATE_CONVERSATION = """CREATE TABLE IF NOT EXISTS conversation
(id_conversation SERIAL PRIMARY KEY, id_receiver INTEGER, id_sender INTEGER,
FOREIGN KEY(id_sender) REFERENCES account (id_account),
FOREIGN KEY(id_receiver) REFERENCES account (id_account));"""

CREATE_MESSAGE = """CREATE TABLE IF NOT EXISTS message
(id_message SERIAL PRIMARY KEY, receiver_sender TEXT, content TEXT, time TEXT, is_read BOOLEAN,
id_conversation INTEGER, FOREIGN KEY(id_conversation) REFERENCES conversation (id_conversation));"""

"""select a.nick as receiver, (select nick from account, conversation
where account.id_account = conversation.id_sender and
c.id_sender = conversation.id_sender) as sender, m.receiver_sender, m."content", m.is_read  from account a
inner join conversation c on a.id_account = c.id_receiver
inner join message m on m.id_conversation = c.id_conversation
where (c.id_receiver = (select aa.id_account from account aa where aa.nick = 'Seba') and
m.receiver_sender = 'send_to_receiver') or c.id_sender  = (select aa.id_account from account aa where aa.nick = 'Seba') and
m.receiver_sender = 'from_receiver';"""