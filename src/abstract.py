import settings

from bs4 import BeautifulSoup

class AbstractManager():
    def __init__(self, driver, secureHash):
        self.driver = driver
        self.secureHash = secureHash

    def get_hp_percentage(self):
        try:
            res = self.driver.request('GET', settings.login_data['index_url'] + f"?mod=overview&sh={self.secureHash}")
            soup = BeautifulSoup(res.text, 'lxml')
            return int(soup.select('div#header_values_hp_percent')[0].text[:-1])
        except Exception as e:
            print("There was an error when trying to read HP in get_hp_percentage(): ", e)
            return 1
