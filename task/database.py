

CREATE_ACCOUNT = """CREATE TABLE IF NOT EXISTS account 
(id_account SERIAL PRIMARY KEY, nick TEXT, password TEXT, admin BOOLEAN);"""

CREATE_CONVERSATION = """CREATE TABLE IF NOT EXISTS conversation
(id_conversation SERIAL PRIMARY KEY, conversation_with TEXT, id_account INTEGER,
FOREIGN KEY(id_account) REFERENCES account (id_account));"""

CREATE_MESSAGE = """CREATE TABLE IF NOT EXISTS message
(id_message SERIAL PRIMARY KEY, receiver_sender TEXT, content TEXT, time TEXT, is_read BOOLEAN,
id_conversation INTEGER, FOREIGN KEY(id_conversation) REFERENCES conversation (id_conversation));"""