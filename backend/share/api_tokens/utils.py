import random
import string
from hashlib import md5


def generate_token(length=15):
    letters = string.ascii_lowercase
    result_str = "".join(random.choice(letters) for _ in range(length))
    return md5(result_str).hexdigest()
