import json
from pprint import pprint


class User:
    BUFFOR_MESSAGES = 5

    def __init__(self):
        self.nick = None
        self.password = None
        self.admin = None
        self.messages = None

    def load_data_from_json(self, nick: str):
        with open("data.json", "r") as file:
            users = json.load(file)
            for userr in users["users"]:
                if userr["nick"] == nick:
                    self.set_data_from_json(**userr)
                    return
            return "No have this user"


    def set_data_from_json(self, nick="default", password="default", admin="default",
                           messages="default"):
        self.nick = nick
        self.password = password
        self.admin = admin
        self.messages = messages

    def print_nick(self):
        print(self.nick, self.password, self.admin)

    def print_messages(self, nick):
        sorted_messages = self.sort_messages_by_date(nick)
        print(f"Conversation with {nick}")
        for from_, text, date in sorted_messages:
            print(from_, text, date)
        only_text = list(map(lambda x: x[1], sorted_messages))
        # pprint(only_text)

    def sort_messages_by_date(self, from_nick="Oli"):
        for text in self.messages:
            if text["from"] == from_nick:
                text["text"] = sorted(text["text"], key=lambda x: x[2])
                return text["text"]

    def check_unread_messages(self):
        for text in self.messages:
            if len(text['unread']) == 0:
                continue
            print(f"You have {len(text['unread'])} unread messages from {text['from']}: ")
            self.read_unread_messages(text)  # we deliver 1 dictionary
            self.sort_messages_by_date(text['from'])
            text["unread"].clear()

    def read_unread_messages(self, messages):
        for num, text in enumerate(messages["unread"]):
            print(num + 1, text)
            text.insert(0, f"from_{messages['from']}")
            self.add_to_read_text(text, messages)

    def add_to_read_text(self, text, messages):
        messages["text"].append(text)

    def update_messages_in_json_file(self):
        with open("data.json", "r") as read:
            users = json.load(read)
            for user in users["users"]:
                if user["nick"] == self.nick:
                    user["messages"] = self.messages
                    break
            with open("data.json", "w") as write:
                json.dump(users, write, indent=4)


user = User()
user.load_data_from_json("Sebaz")

user.print_messages("Olii")
user.check_unread_messages()
user.print_messages("Olii")

# user.update_messages_in_json_file() # dziala

"""
TODO

wysyłanie wiadomosci
cos z adminem i uprawnieniami
usuwanie/dodawanie(rejestracja) uzytkownikow
logowanie i wylogowywanie

"""

"""
przepełnienie 5 wiadomosci zrobiłem tak, że każdy uzytkownik moze wysłać bez odczytania max 5 wiadomosci
do odbiorcy, czyli jeżeli wysyła dwóch nadawców to maksymalnie odbiora ma do odczytu 10 wiadomosci,

można bylo by zrobic że te 5 wiadomosci to sumaryczna liczba nieodczytanych wiadomosci od wszystkich nadawców,
ale wybrałem opcje 1szą.

"""
