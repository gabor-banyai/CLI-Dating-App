import sys
import os
import json
import getpass
from collections import namedtuple

import encoder
from user import User, Gender

USERS_FILE = "users.json"
INTERESTS_FILE = "interests.txt"

INVALID_OPTION_STR = "Invalid option, please select one of the\n" \
                     "available options."


def find_match():
    global current_user
    u = current_user
    match = False

    with open(USERS_FILE) as f:
        data = json.load(f)
        for p in data:
            pu = encoder.as_user(p)
            if pu.username != u.username:
                common = set(u.interests) & set(pu.interests)
                # Match if they have common interests or if the user who does the query does not have any interest
                common_match = u.interests == [] or len(common) > 0
                if int(u.pref_age_min) <= int(pu.age) <= int(u.pref_age_max) and \
                        int(pu.pref_age_min) <= int(u.age) <= int(pu.pref_age_max) and\
                        u.gender == pu.pref_gender and\
                        u.pref_gender == pu.gender and\
                        common_match:
                    if not match:
                        print('Matched with: ')
                        match = True
                    print('Username: ', pu.username)
                    print('Name: ', pu.name)
                    if len(common) > 0:
                        print("Common interests are:")
                        print(common)

    if not match:
        print('There is no match for you. Sorry!')


def query():
    find_match()
    show_view('home')


def save_user():
    global current_user
    if current_user:
        with open(USERS_FILE) as f:
            temp = json.load(f)
            temp.append(current_user.__dict__)
            f.close()
        file = open(USERS_FILE, 'w+')
        json.dump(temp, file, cls=encoder.EnumEncoder, indent=0)
        file.close()


def input_min(s, condition, msg, ispass = False):
    str = ""
    while not condition(str):
        str = input(s) if not ispass else getpass.getpass(s)
        if is_quit(str):
            sys.exit(0)
        if not condition(str):
            print(msg)

    return str

def input_str_chars(s, ispass = False):
    non_empty_func = lambda s: len(s) >= 6 and len(s) <= 20 and s.isalnum()
    non_empty_err = 'Please try again, input should between 6 and 20 characters and\n' \
                    'only numbers and letters allowed.'
    return input_min(s, non_empty_func, non_empty_err, ispass)


def input_str_letters(s):
    non_empty_func = lambda s: len(s) >= 3 and len(s) <= 20 and s.isalpha()
    non_empty_err = 'Please try again, input should between 3 and 20 characters and\n' \
                    'only letters are allowed.'
    return input_min(s, non_empty_func, non_empty_err)


def add_interest():
    print('Let\'s choose some interests')
    interests = []
    while True:
        print('[1] Add interest')
        print('[2] Finish adding interests')
        choice = input_min('', lambda a: a.isnumeric() and 1 <= int(a) <= 2, INVALID_OPTION_STR)
        if choice == '1':
            interests.append(input_str_letters("Please enter an interest:"))
        else:
            break
    return interests


def get_uniq_username():
    unique = False
    username = ''

    while not unique:
        username = input_str_chars("Please enter username: ")
        found = False
        with open(USERS_FILE) as f:
            data = json.load(f)
            for p in data:
                if p['username'] == username:
                    found = True
                    break
        if not found:
            unique = True
        else:
            print('Username already exists.')
    return username

def handle_register():
    username = get_uniq_username()
    password = input_str_chars("Please enter password: ")
    password = encoder.hash_pass(password)

    name = input_str_letters("Please enter name: ")

    age_func = lambda a: a.isnumeric() and 18 <= int(a) < 200
    age_err = 'Minimum age is 18, maximum age is 199'
    age = int(input_min("Please enter age: ", age_func, age_err))

    gender_str = 'Please enter gender by typing the corresponding number' \
                 '\n[1] FEMALE\n[2] MALE\n[3] NONBINARY\n'
    gender_func = lambda a: a.isnumeric() and 1 <= int(a) <= 3
    gender = Gender(int(input_min(gender_str, gender_func, "Option is not valid.")))

    pref_gender_str = 'Please enter preferred gender by typing the corresponding number' \
                      '\n[1] FEMALE\n[2] MALE\n[3] NONBINARY\n'
    pref_gender = Gender(int(input_min(pref_gender_str, gender_func, "Option is not valid.")))

    valid_age = False

    while not valid_age:
        pref_age_min = int(input_min("Please enter preferred minimum age: ", age_func, age_err))
        pref_age_max = int(input_min("Please enter preferred maximum age: ", age_func, age_err))
        if pref_age_min <= pref_age_max:
            valid_age = True
        else:
            print('Please make sure the minimum age is lower (or equal) than the maximum age!')

    interests = add_interest()

    global current_user
    current_user = User(name, username, password, age, gender, interests, pref_age_min, pref_age_max, pref_gender)
    show_view('home')


def login():
    loggedin = False
    MAX_RETRIES = 3
    retries = 0
    global current_user

    while retries < MAX_RETRIES and not loggedin:
        retries += 1
        with open(USERS_FILE) as f:
            username = input_str_chars("Please enter username: ")
            password = input_str_chars("Please enter password: ")
            data = json.load(f)
            #print(data)
            for p in data:
                if p['username'] == username and encoder.verify_pass(p['password'], password):
                    loggedin = True
                    break
            if not loggedin and retries != MAX_RETRIES:
                print("Wrong username or password. Please try again")

    if not loggedin:
        print("Maximum number of retries reached. Please try again later")
        show_view('home')
    else:
        print("Successful login!")
        current_user = encoder.as_user(p)
        show_view('home')


def show_view(view_name):
    global current_user

    # os.system('clear')
    # print("------------------------ ♥ ------------------------")
    # print("                   Dating Project                  ")
    # print("---------------------------------------------------")

    if view_name == 'home':

        if current_user:
            print("You are logged in as {}".format(current_user.username))
        print("Please enter one of the following commands         ")
        print("by specifying a number.                            ")
        print()

        if current_user:
            print("[3] exit")
            print("[4] query")
            print("[5] logout")
        else:
            print("[1] register")
            print("[2] login")
            print("[3] exit")

    elif view_name == 'register':
        handle_register()
        save_user()

    elif view_name == 'login':
        login()

    elif view_name == 'query':
        query()

    elif view_name == 'logout':
        # save_user() # Do not edit users at this time
        current_user = None
        show_view('home')

    elif view_name == 'exit':
        # save_user() # Do not edit users at this time
        print("Thank you for using our application, see you soon!")
        sys.exit(0)


def is_quit(choice):
    return choice == 'q' or choice == 'quit'


if __name__ == "__main__":
    global current_user
    current_user = None

    # we need to check if files are in the . folder before starting the program
    # tried making a standalone executable with pyinstaller and it crashed because of this
    # it's good for the user to be prompted with an error message as well

    if not os.path.isfile(USERS_FILE):
        print("{} is missing from current directory.".format(USERS_FILE))
        sys.exit(0)

    choice = ''

    print("------------------------ ♥ ------------------------")
    print("                   Dating Project                  ")
    print("---------------------------------------------------")
    show_view('home')

    while not is_quit(choice):
        choice = input()
        if is_quit(choice):
            break

        # Separate commands based on whether or not the user is authenticated.
        if not current_user:
            if choice == "1" or choice == "[1]":
                show_view('register')
            elif choice == "2" or choice == "[2]":
                show_view('login')
            elif choice == "3" or choice == "[3]":
                show_view('exit')
            else:
                print(INVALID_OPTION_STR)
        else:
            if choice == "3" or choice == "[3]":
                show_view('exit')
            elif choice == "4" or choice == "[4]":
                show_view('query')
            elif choice == "5" or choice == "[5]":
                show_view('logout')
            else:
                print(INVALID_OPTION_STR)

    print("Thank you for using our application, see you soon!")
    sys.exit(0)

