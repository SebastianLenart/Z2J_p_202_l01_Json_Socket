from connect_sql import GetConnection
import database
import json
from pprint import pprint


class User:
    BUFOR_MESSAGES = 5

    def __init__(self):
        self.nick = None
        self.password = None
        self.admin = None
        self.messages = None
        self.users_file = None

    # add to new user can only admin
    def register_new_user(self, nick="Default", password="1234", admin=False):
        with GetConnection() as connection:
            if not self.admin:
                print(f"Only admin can add new user!")
                return f"Only admin can add new user!"
            for user in database.get_list_nicks(connection):
                if user[0] == nick:
                    return f"This nick is busy."
            new_user = {
                "nick": nick,
                "password": password,
                "admin": admin
            }
            return_value = database.add_new_user(connection, **new_user)
            pprint(return_value)
            return f"Register done!"

    def show_list_users(self):
        with GetConnection() as connection:
            return [element[0] for element in database.get_list_nicks(connection)]

    def show_base_info_about(self, nick):
        if self.admin != "admin":
            return f"Only admin can get info!"
        with GetConnection() as connection:
            return database.get_base_info(connection, nick)

    def login(self, nick: str = "Default", password: str = "1234"):
        with GetConnection() as connection:
            if nick not in [element[0] for element in database.get_list_nicks(connection)]:
                return f"Not found user {nick}"
            user = database.get_base_info(connection, nick)  # powyzsze linijki sa zbedne przy tym zapisie..
            if user[0] == nick and user[1] == password:
                self.set_data_from_db(*user)
                return f"Login"
        return f"Password is wrong"

    def check_user_exists(self, nick="Olaf"):
        with GetConnection() as connection:
            for user in database.get_list_nicks(connection):
                if user[0] == nick:
                    return True
            # raise SomethingWrong(f"Not found user {nick}")
            return False

    def set_data_from_db(self, nick="default", password="default", admin="False"):
        self.nick = nick
        self.password = password
        self.admin = admin

    # def print_nick(self):
    #     print(self.nick, self.password, self.admin)

    def show_conversation(self, nick="Olaf"):
        if not self.check_do_u_have_this_nick_in_conversation(nick):  # dodaj self.nick
            print("You dont have this nick in conversation")
            return
        self.check_unread_messages()
        self.read_unread_messages()
        sorted_messages = self.sort_messages_by_date(nick)
        print(f"Conversation with {nick}:")
        if len(sorted_messages) == 0:
            print("- Empty")
        only_text = list(map(lambda x: x[3], sorted_messages))
        # pprint(only_text)
        return sorted_messages

    def sort_messages_by_date(self, from_nick="Olaf"):
        with GetConnection() as connection:
            messages_from_sb = database.get_conversation_by_nick(connection)  # dodaj nicki!!!!
            # messages_from_sb_sort_reverse = sorted(messages_from_sb, key=lambda x: x[4], reverse=True)
            # pprint(messages_from_sb_sort_reverse)
            return messages_from_sb

    def check_unread_messages(self):
        with GetConnection() as connection:
            counter_unread = database.get_counter_unread_messages(
                connection)  # dodaj self.nick ale dopiero po zalogowaniu!!!
            if len(counter_unread) == 0:
                return []
            for unread in counter_unread:
                print(f"You {unread[0]} have {unread[2]} messages from {unread[1]}")
            return counter_unread

    def read_unread_messages(self):
        with GetConnection() as connection:
            unread_messages = database.get_unread_messages(connection)  # dodaj self.nick ale dopiero po zalogowaniu!!!
            for text in unread_messages:
                print(f"{text[0]} have unread message(s) from {text[3]}: {text[4]}")
                database.update_unread_message(connection, text[2])
        return unread_messages

    # def add_to_read_text(self, text, messages):
    #     messages["text"].append(text)

    # def update_messages_in_json_file(self):
    #     for user in self.users_file["users"]:
    #         if user["nick"] == self.nick:
    #             user["messages"] = self.messages
    #             break
    #     with open("data.json", "w") as write:
    #         json.dump(self.users_file, write, indent=4)  # dziwne, inne usery tez sie zapisuja, ale to dobrze!

    def check_bufor_in_receiver(self, nick="Olaf"):
        with GetConnection() as connection:
            counter_unread_messages = database.get_counter_unread_messages_with_sb(connection)  # dodaj nicki!!!
            if counter_unread_messages[2] >= self.BUFOR_MESSAGES:
                return True
            return False

    def send_text_to(self, send_to_nick="Olaf", text: list = ["sth"]):
        if not self.check_user_exists(send_to_nick):
            return f"Not found user {send_to_nick}"  # niemożemy wyslac do osoby ktora nie istnieje
        if self.check_bufor_in_receiver(send_to_nick):
            return f"Bufor is full, you cant sent text"

        with GetConnection() as connection:
            sender_or_receiver = database.determine_sender_or_receiver(connection)[0]
            text.insert(0, f"{sender_or_receiver[1]}")
            if not self.check_do_u_have_this_nick_in_conversation(send_to_nick):  # dodaj self.nick
                print("You dont have this nick in conversation, Now it's going to be added")
                print(database.add_conversation(connection)) # dodaj nicki!!!




            # save data in my profil and his/her profil as well
            # conversation_person["text"].append(text)
            # text2 = text[:]
            # text2[0] = f"from_{self.nick}"
            # self.save_unread_text_in_receiver(send_to_nick, text2)
            # self.update_messages_in_json_file()
            # return f"Send ok"

    def check_do_u_have_this_nick_in_conversation(self, nick="Olaf"):
        with GetConnection() as connection:
            list_users = database.get_nicks_conversation(connection)  # dodaj self.nick ale dopiero po zalogowaniu!!!
            for user in list_users:
                if nick == user[0]:
                    return True
            return False
            # self.messages.append({
            #     "with": nick,
            #     "unread": [],
            #     "text": []
            # })
            # return self.messages[-1]

    def save_unread_text_in_receiver(self, nick, text: list):
        for user_dict in self.users_file["users"]:
            if user_dict["nick"] == nick:
                conversation_person = self.check_do_u_have_this_nick_in_conversation(self.nick, user_dict["messages"])
                conversation_person["unread"].append(text)


if __name__ == '__main__':
    user = User()
    pprint(user.send_text_to())

"""
if __name__ == '__main__':  # !!! bez tego ponizsze linijki beda wywolywane gdy gdzies uzyjemy 'from user import User'
    user = User()
    print(user.login("Seba", "qaz123"))
    # print(user.login("Olaf", "qaz321"))
    # user.check_unread_messages()
    # user.send_text_to("Olaf", ["wiadomosc", "17"])
    # user.show_conversation("Olaf")

"""
