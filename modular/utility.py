
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

def get_hp_percentage():
    res = driver.request('GET', login_data['index_url'] + f"?mod=overview&sh={secureHash}")
    soup = BeautifulSoup(res.text, 'html5lib')
    return int(soup.select('div#header_values_hp_percent')[0].text[:-1])

def get_milliseconds():
    return int(round(time.time() * 1000))
