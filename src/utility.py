import time
import settings

"""
Utility functions
"""

def get_hash(text):
    i = text.find("secureHash")
    secureHash = ""
    OK = 2
    while OK:
        if text[i] == "=":
            i += 2
            while OK:
                if text[i] == '"':
                    OK -= 1
                else:
                    secureHash += text[i]
                i += 1
        i += 1
    return secureHash
def get_milliseconds():
    return int(round(time.time() * 1000))
