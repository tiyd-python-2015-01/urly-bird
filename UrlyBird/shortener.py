from hashids import Hashids
from random import randint

#wtf is a salt?
hashids = Hashids(salt = "a nice salt")

def shortener():
    rand_list = [randint(1,10) for _ in range(3)]
    id = hashids.encode(*rand_list)
    return id
