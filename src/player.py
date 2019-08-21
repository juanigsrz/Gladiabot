import enum
import settings, utility

from abstract import AbstractManager
from bs4 import BeautifulSoup

class PlayerManager(AbstractManager):
    """
    Player overall stats management
    """
    def get_hp_percentage(self):
        try:
            res = self.driver.request('GET', settings.login_data['index_url'] + f"?mod=overview&sh={self.secureHash}")
            soup = BeautifulSoup(res.text, 'lxml')
            return int(soup.select('div#header_values_hp_percent')[0].text[:-1])
        except Exception as e:
            print("There was an error when trying to read HP in get_hp_percentage(): ", e)
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
                self.async_request('POST', settings.login_data['index_url'] + f"?mod=training&submod=train&skillToTrain={skills[s].value}&sh={self.secureHash}", {})
            print(f"Tried to train skills successfully!")
            return True
        except Exception as e:
            print("Couldn't train in go_training()! Error: ", e)
            return False
