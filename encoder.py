import json
import hashlib
import os
import binascii
from user import Gender, User

PUBLIC_ENUMS = {
    'Gender': Gender,
    # ...
}


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if type(obj) in PUBLIC_ENUMS.values():
            return {"__enum__": str(obj)}
        return json.JSONEncoder.default(self, obj)


def as_enum(d):
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return getattr(PUBLIC_ENUMS[name], member)
    else:
        return d


def as_user(d):
    return User(name=d["name"], username=d["username"], password=d["password"], age=d["age"], gender=as_enum(d["gender"]),
                pref_age_min=d["pref_age_min"], pref_age_max=d["pref_age_max"], pref_gender=as_enum(d["pref_gender"]),
                interests=d['interests'])

def hash_pass(password):
    salt = hashlib.sha256(os.urandom(25)).hexdigest().encode('ascii')
    hashed_pass = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    hashed_pass = binascii.hexlify(hashed_pass)
    return (salt + hashed_pass).decode('ascii')

def verify_pass(stored, provided):
    salt = stored[:64]
    stored_password = stored[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password
