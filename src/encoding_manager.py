import base64
import hashlib
import string
from random import choices


# Generate a [0-9a-zA-Z] string
ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def encode(id_number, alphabet=ALPHABET):
    """Convert an integer to a string."""
    if id_number == 0:
        return alphabet[0]

    alphabet_len = len(alphabet) # Cache

    result = ''
    while id_number > 0:
        id_number, mod = divmod(id_number, alphabet_len)
        result = alphabet[mod] + result

    return result


def decode(id_string, alphabet=ALPHABET):
    """Convert a string to an integer."""
    alphabet_len = len(alphabet) # Cache
    return sum([alphabet.index(char) * pow(alphabet_len, power) for power, char in enumerate(reversed(id_string))])


def generate_short_url():
    characters = string.digits + string.ascii_letters
    short_url = ''.join(choices(characters, k=6))
    return short_url
