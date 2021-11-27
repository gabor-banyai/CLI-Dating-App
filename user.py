from enum import Enum

PREF_AGE_MIN = 18
PREF_AGE_MAX = 200


class Gender(Enum):
    FEMALE = 1
    MALE = 2
    NONBINARY = 3


class Interests(Enum):
    PHOTOGRAPHY = 1
    SPORT = 2
    MUSIC = 3


class User:

    def __init__(self, name, username, password, age, gender,
                 interests, pref_age_min, pref_age_max, pref_gender):
        self.name = name
        self.username = username
        self.password = password
        self.age = age
        self.gender = gender
        self.interests = interests
        self.pref_age_min = pref_age_min
        self.pref_age_max = pref_age_max
        self.pref_gender = pref_gender



