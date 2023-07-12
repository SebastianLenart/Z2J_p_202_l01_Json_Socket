from user import User

def test_fortest():
    a = 2
    assert a == 2


def test_register_new_user_no_admin():
    user = User()
    answer = user.register_new_user()
    assert answer == f"Only admin can add new user!"

def test_test_register_new_user():
    user = User()
    user.admin = "admin"
    user.users_file = {"users": []} # or some random users only for tests
    answer = user.register_new_user("nick1", "qwe", "no admin")
    assert answer == f"Register done!"

def test_show_list_users():
    user = User()
    user.users_file = {"users": ["Seba"]}
    assert len(user.show_list_users()) == 1

def test_show_base_info_about():
    user = User()
    user.admin = "admin"
    user.users_file = {"users": []}





"""
testy musza byc w tym samym folderze!
python -m pytest test_users.py -vvv



"""









