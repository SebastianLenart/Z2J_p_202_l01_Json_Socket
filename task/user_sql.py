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
            # if not self.admin:
            #     print(f"Only admin can add new user!")
            #     return f"Only admin can add new user!"
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
        return self.users_file["users"]

    def show_base_info_about(self, nick):
        if self.admin != "admin":
            return f"Only admin can get info!"
        for user in self.users_file["users"]:
            if user["nick"] == nick:
                return f"{user['nick']}, {user['password']}, {user['admin']}"

    def login(self, nick: str = "default", password: str = "1234"):
        with open("data.json", "r") as file:
            self.users_file = json.load(file)
            if not self.check_user_exists(self.users_file["users"], nick):
                return f"Not found user {nick}"
            for userr in self.users_file["users"]:
                if userr["nick"] == nick and userr["password"] == password:
                    self.set_data_from_json(**userr)
                    return f"Login"
                else:
                    continue
            return f"Password is wrong"

    def check_user_exists(self, list_users, nick):
        for user_dict in list_users:
            if user_dict["nick"] == nick:
                return True
        # raise SomethingWrong(f"Not found user {nick}")
        return False

    def set_data_from_json(self, nick="default", password="default", admin="No admin",
                           messages="default"):
        self.nick = nick
        self.password = password
        self.admin = admin
        self.messages = messages

    def print_nick(self):
        print(self.nick, self.password, self.admin)

    def show_conversation(self, nick):
        self.check_do_u_have_this_nick_in_conversation(nick, self.messages)
        self.check_unread_messages() # odczytuje nieodczytane, ale wszystkie, nie tylko od tego konkretnego usera...
        sorted_messages = self.sort_messages_by_date(nick)
        print(f"Conversation with {nick}")
        return_list = []
        for from_, text, date in sorted_messages:
            return_list.append([from_, text, date])
        if not return_list:
            print("- Empty")
        only_text = list(map(lambda x: x[1], sorted_messages))
        # pprint(only_text)
        return return_list

    def sort_messages_by_date(self, from_nick="Oli"):
        for text in self.messages:
            if text["with"] == from_nick:
                text["text"] = sorted(text["text"], key=lambda x: x[2])
                return text["text"]

    def check_unread_messages(self):
        return_unread_texts = []
        for text in self.messages:
            if len(text['unread']) == 0:
                continue
            print(f"You have {len(text['unread'])} unread messages from {text['with']}: ")
            return_unread_texts = self.read_unread_messages(text)  # we deliver 1 dictionary
            self.sort_messages_by_date(text['with'])
            text["unread"].clear()
        self.update_messages_in_json_file()
        return return_unread_texts

    def read_unread_messages(self, messages):
        return_list = []
        for num, text in enumerate(messages["unread"]):
            print(num + 1, text)
            return_list.append(text)
            self.add_to_read_text(text, messages)
        return return_list

    def add_to_read_text(self, text, messages):
        messages["text"].append(text)

    def update_messages_in_json_file(self):
        for user in self.users_file["users"]:
            if user["nick"] == self.nick:
                user["messages"] = self.messages
                break
        with open("data.json", "w") as write:
            json.dump(self.users_file, write, indent=4)  # dziwne, inne usery tez sie zapisuja, ale to dobrze!

    def check_bufor_in_receiver(self, nick):
        for user_dict in self.users_file["users"]:
            if user_dict["nick"] == nick:
                for conversation in user_dict["messages"]:
                    if conversation["with"] == self.nick:
                        if len(conversation["unread"]) >= self.BUFOR_MESSAGES:
                            return True
        return False

    def send_text_to(self, send_to_nick, text: list):
        if not self.check_user_exists(self.users_file["users"], send_to_nick):
            return f"Not found user {send_to_nick}" # niemożemy wyslac do osoby ktora nie istnieje
        if self.check_bufor_in_receiver(send_to_nick):
            return f"Bufor is full, you cant sent text"
        text.insert(0, f"send_to_{send_to_nick}")
        conversation_person = self.check_do_u_have_this_nick_in_conversation(send_to_nick, self.messages)
        # save data in my profil and his/her profil as well
        conversation_person["text"].append(text)
        text2 = text[:]
        text2[0] = f"from_{self.nick}"
        self.save_unread_text_in_receiver(send_to_nick, text2)
        self.update_messages_in_json_file()
        return f"Send ok"

    def check_do_u_have_this_nick_in_conversation(self, nick, messages):
        for mess_disct in messages:
            if mess_disct["with"] == nick:
                return mess_disct
        self.messages.append({
            "with": nick,
            "unread": [],
            "text": []
        })
        return self.messages[-1]

    def save_unread_text_in_receiver(self, nick, text: list):
        for user_dict in self.users_file["users"]:
            if user_dict["nick"] == nick:
                conversation_person = self.check_do_u_have_this_nick_in_conversation(self.nick, user_dict["messages"])
                conversation_person["unread"].append(text)






if __name__ == '__main__':
    user = User()
    user.register_new_user()




"""
if __name__ == '__main__':  # !!! bez tego ponizsze linijki beda wywolywane gdy gdzies uzyjemy 'from user import User'
    user = User()
    print(user.login("Seba", "qaz123"))
    # print(user.login("Olaf", "qaz321"))
    # user.check_unread_messages()
    # user.send_text_to("Olaf", ["wiadomosc", "17"])
    # user.show_conversation("Olaf")

"""




































