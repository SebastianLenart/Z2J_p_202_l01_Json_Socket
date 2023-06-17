import json
from pprint import pprint
from exception import SomethingWrong


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
        if not self.admin:
            print(f"Only admin can add new user!")
            return f"Only admin can add new user!"
        for user in self.users_file["users"]:
            if user["nick"] == nick:
                print("This nick is busy.")
                return f"This nick is busy."
        new_user = {
            "nick": nick,
            "password": password,
            "admin": admin,
            "messages": []
        }
        self.users_file["users"].append(new_user)
        with open("data.json", "w") as write:
            json.dump(self.users_file, write, indent=4)  # dziwne, inne usery tez sie zapisuja, ale to dobrze!

    def show_list_users(self):
        return self.users_file["users"]

    def show_base_info_about(self, nick):
        if not self.admin:
            print(f"Only admin can get info!")
        for user in self.users_file["users"]:
            if user["nick"] == nick:
                return [user["nick"], user["password"], user["admin"]]

    def login(self, nick: str, password):
        with open("data.json", "r") as file:
            self.users_file = json.load(file)
            self.check_user_exists(self.users_file["users"], nick)
            for userr in self.users_file["users"]:
                if userr["nick"] == nick and userr["password"] == password:
                    self.set_data_from_json(**userr)
                    return

    def check_user_exists(self, list_users, nick):
        for user_dict in list_users:
            if user_dict["nick"] == nick:
                return True
        raise SomethingWrong(f"Not found user {nick}")

    def set_data_from_json(self, nick="default", password="default", admin="default",
                           messages="default"):
        self.nick = nick
        self.password = password
        self.admin = admin
        self.messages = messages

    def print_nick(self):
        print(self.nick, self.password, self.admin)

    def show_conversation(self, nick):
        sorted_messages = self.sort_messages_by_date(nick)
        print(f"Conversation with {nick}")
        for from_, text, date in sorted_messages:
            print(from_, text, date)
        only_text = list(map(lambda x: x[1], sorted_messages))
        # pprint(only_text)

    def sort_messages_by_date(self, from_nick="Oli"):
        for text in self.messages:
            if text["with"] == from_nick:
                text["text"] = sorted(text["text"], key=lambda x: x[2])
                return text["text"]

    def check_unread_messages(self):
        for text in self.messages:
            if len(text['unread']) == 0:
                continue
            print(f"You have {len(text['unread'])} unread messages from {text['with']}: ")
            self.read_unread_messages(text)  # we deliver 1 dictionary
            self.sort_messages_by_date(text['with'])
            text["unread"].clear()

    def read_unread_messages(self, messages):
        for num, text in enumerate(messages["unread"]):
            print(num + 1, text)
            text.insert(0, f"from_{messages['with']}")
            self.add_to_read_text(text, messages)

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
        self.check_user_exists(self.users_file["users"], send_to_nick)  # niemożemy wyslac do osoby ktora nie istnieje
        if self.check_bufor_in_receiver(send_to_nick):
            print(f"Bufor is full, you cant sent texts")
            return f"Bufor is full, you cant sent textt"
        text.insert(0, f"send_to_{send_to_nick}")
        conversation_person = self.check_do_u_have_this_nick_in_conversation(send_to_nick, self.messages)
        # save data in my profil and his/her profil as well
        conversation_person["text"].append(text)
        text[0] = f"from_{self.nick}"
        self.save_unread_text_in_receiver(send_to_nick, text)
        # self.update_data_in_json()

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


if __name__ == '__main__': # !!! bez tego ponizsze linijki beda wywolywane gdy gdzies uzyjemy 'from user import User'
    user = User()
    user.login("Seba", "qaz123")
    # user.show_conversation("Olii")
    user.check_unread_messages()
    # user.show_conversation("Olii")
    user.send_text_to("Olaf", ["wiadomosc", "16"])
    # user.register_new_user()
    user.update_messages_in_json_file()  # dziala

"""
TODO
usuwanie/dodawanie(rejestracja) uzytkownikow # potem usuwanie dokonczyc
logowanie i wylogowywanie
przenies potem dane do postgresqla
"""

"""
przepełnienie 5 wiadomosci zrobiłem tak, że każdy uzytkownik moze wysłać bez odczytania max 5 wiadomosci
do odbiorcy, czyli jeżeli wysyła dwóch nadawców to maksymalnie odbiorca ma do odczytu 10 wiadomosci,

można bylo by zrobic że te 5 wiadomosci to sumaryczna liczba nieodczytanych wiadomosci od wszystkich nadawców,
ale wybrałem opcje 1szą.


teorytycznie nadawca i odbiorca powinni miec identyczna historie konwersacji miedzy sobą..
Dopóki nie zmodyfikuje jsona to algorytm powiniem tak zadzialac

"""
