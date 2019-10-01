import enum, re
import settings, utility

from abstract import AbstractManager
from bs4 import BeautifulSoup

class PlayerManager(AbstractManager):
    """
    Player overall stats management
    """
    def is_arena_ready(self):
        try:
            res = self.driver.request('GET', settings.login_data['index_url'] + f"?mod=overview&sh={self.secureHash}")
            soup = BeautifulSoup(res.text, 'lxml')
            string_to_check = soup.select('div#cooldown_bar_text_arena')[0].text
            return (not (string_to_check == "-" or bool(re.match(r"[0-9]+:[0-9]+:[0-9]+", string_to_check))))
        except Exception as e:
            print("There was an error when trying to read arena status in is_arena_ready(): ", e)
            return False
    def is_circus_ready(self):
        try:
            res = self.driver.request('GET', settings.login_data['index_url'] + f"?mod=overview&sh={self.secureHash}")
            soup = BeautifulSoup(res.text, 'lxml')
            string_to_check = soup.select('div#cooldown_bar_text_ct')[0].text
            return (not (string_to_check == "-" or bool(re.match(r"[0-9]+:[0-9]+:[0-9]+", string_to_check))))
        except Exception as e:
            print("There was an error when trying to read circus status in is_circus_ready(): ", e)
            return False
    def is_expedition_ready(self):
        try:
            res = self.driver.request('GET', settings.login_data['index_url'] + f"?mod=overview&sh={self.secureHash}")
            soup = BeautifulSoup(res.text, 'lxml')
            string_to_check = soup.select('div#cooldown_bar_text_expedition')[0].text
            return self.get_expedition_points() > 0 and (not (string_to_check == "-" or bool(re.match(r"[0-9]+:[0-9]+:[0-9]+", string_to_check))))
        except Exception as e:
            print("There was an error when trying to read expedition status in is_expedition_ready(): ", e)
            return False
    def is_dungeon_ready(self):
        try:
            res = self.driver.request('GET', settings.login_data['index_url'] + f"?mod=overview&sh={self.secureHash}")
            soup = BeautifulSoup(res.text, 'lxml')
            string_to_check = soup.select('div#cooldown_bar_text_dungeon')[0].text
            return self.get_dungeon_points() > 0 and (not (string_to_check == "-" or bool(re.match(r"[0-9]+:[0-9]+:[0-9]+", string_to_check))))
        except Exception as e:
            print("There was an error when trying to read dungeon status in is_dungeon_ready(): ", e)
            return False
    def get_hp_percentage(self):
        try:
            res = self.driver.request('GET', settings.login_data['index_url'] + f"?mod=overview&sh={self.secureHash}")
            soup = BeautifulSoup(res.text, 'lxml')
            return int(soup.select('div#header_values_hp_percent')[0].text[:-1])
        except Exception as e:
            print("There was an error when trying to read HP in get_hp_percentage(): ", e)
            return -1
    def get_expedition_points(self):
        try:
            res = self.driver.request('GET', settings.login_data['index_url'] + f"?mod=overview&sh={self.secureHash}")
            soup = BeautifulSoup(res.text, 'lxml')
            return int(soup.select('span#expeditionpoints_value_point')[0].text)
        except Exception as e:
            print("There was an error when trying to read expedition points in get_expedition_points(): ", e)
            return -1
    def get_dungeon_points(self):
        try:
            res = self.driver.request('GET', settings.login_data['index_url'] + f"?mod=overview&sh={self.secureHash}")
            soup = BeautifulSoup(res.text, 'lxml')
            return int(soup.select('span#dungeonpoints_value_point')[0].text)
        except Exception as e:
            print("There was an error when trying to read expedition points in get_expedition_points(): ", e)
            return -1
    def purchase_gods_favours(self, gods_to_purchase = [], favour_rank = 2):
        print("Let's try to purchase gods favours!")
        try:
            gods = enum.Enum('gods', ['Minerva', 'Diana', 'Vulcan', 'Mars', 'Apollo', 'Mercury'], start = 1)
            for g in gods_to_purchase:
                self.async_request('POST', settings.login_data['index_url'] + f"?mod=gods&submod=activateBlessing&god={gods[g].value}&rank={favour_rank}&sh={self.secureHash}", {})
            print(f"Finished trying to purchase gods' favours!")
            return True
        except Exception as e:
            print("There was a problem on purchase_gods_favours(): ", e)
            return False
    def go_training(self, skills_to_train = []):
        print("Let's go training!")
        try:
            skills = enum.Enum('skills', ['Strength', 'Dexterity', 'Agility', 'Constitution', 'Charisma', 'Intelligence'], start = 1)
            for s in skills_to_train:
                # self.async_request('POST', settings.login_data['index_url'] + f"?mod=training&submod=train&skillToTrain={skills[s].value}&sh={self.secureHash}", {})
                self.driver.request('POST', settings.login_data['index_url'] + f"?mod=training&submod=train&skillToTrain={skills[s].value}&sh={self.secureHash}")
            print(f"Tried to train skills successfully!")
            return True
        except Exception as e:
            print("Couldn't train in go_training()! Error: ", e)
            return False
