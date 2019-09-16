import random
import string

def generateRandomLowerString():
    string_length = random.randint(10, 20)
    letters = string.ascii_lowercase

    return ''.join(random.choice(letters) for i in range(string_length))