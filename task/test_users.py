from user import User


def test_fortest():
    a = 2
    assert a == 2


def test_register_new_user_no_admin():
    user = User()
    answer = user.register_new_user()
    assert answer == f"Only admin can add new user!"


def test_show_list_users():
    user = User()
    user.users_file = {"users": ["Seba"]}
    assert len(user.show_list_users()) == 1


def test_show_base_info_about():
    user = User()
    user.admin = "admin"
    new_user = {
        "nick": "nick1",
        "password": "password1",
        "admin": "admin1",
        "messages": []
    }
    user.users_file = {"users": [new_user]}
    result = user.show_base_info_about("nick1")
    assert result == f"nick1, password1, admin1"


def test_login():
    user = User()
    result = user.login("Seba", "qaz123")
    assert result == f"Login"


def test_show_conversation():
    user = User()
    user.nick = "Seba"
    user.messages = []
    user.users_file = {"users": []}
    result = user.show_conversation("aaa")
    # assert result == []
    assert len(result) == 0


def test_check_unread_messages():
    user = User()
    user.nick = "Seba"
    user.messages = [
        {
            "with": "Olaf",
            "unread": [
                [
                    "send_to_receiver",
                    "Hello reveiver",
                    "2023-06-11 12:56:59"
                ]
            ],
            "text": []
        }
    ]
    user.users_file = {"users": []}
    result = user.check_unread_messages()[0]
    assert result ==  [
                    "send_to_receiver",
                    "Hello reveiver",
                    "2023-06-11 12:56:59"
                ]


# musi byc na koncu bo nadpisuje plik data.json
# po tym tescie resetuje sie plik data.json trzeba go przywrocic
def test_test_register_new_user():
    user = User()
    user.admin = "admin"
    user.users_file = {"users": []}  # or some random users only for tests
    answer = user.register_new_user("nick1", "qwe", "no admin")
    assert answer == f"Register done!"


"""
testy musza byc w tym samym folderze!
python -m pytest test_users.py -vvv



"""
