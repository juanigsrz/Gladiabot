import settings, utility, translation

from bs4 import BeautifulSoup
from abstract import AbstractManager

class ExpeditionManager(AbstractManager):
    """
    Expedition
    """
    def go_expedition(self, location, stage):
        print("Let's go into an expedition!")
        try:
            self.driver.request('POST', settings.login_data['ajax_url'] + f"?mod=location&submod=attack&location={location}&stage={stage}&premium=0&a={utility.get_milliseconds()}&sh={self.secureHash}")
            #self.async_request('POST', settings.login_data['ajax_url'] + f"?mod=location&submod=attack&location={location}&stage={stage}&premium=0&a={utility.get_milliseconds()}&sh={self.secureHash}", {})
        except Exception as e:
            print("There was a a problem on go_expedition(): ", e)
            return
        print("Finished going to the expedition!")

    """
    Dungeons
    """
    def go_dungeon(self, location, dungeon_name, posi_sequence, difficulty, skip_boss):
        print(f"Let's go to {dungeon_name}!")

        try:
            if difficulty != translation.dungeon_normal_text and difficulty != translation.dungeon_advanced_text:
                raise "Difficulty not found!"

            self.driver.request('POST', settings.login_data['index_url'] + f"?mod=dungeon&loc={location}&sh={self.secureHash}",
                                data = {('dif1' if difficulty == translation.dungeon_normal_text else 'dif2'): difficulty})
            res = self.driver.request('GET', settings.login_data['index_url'] + f"?mod=dungeon&loc={location}&sh={self.secureHash}")

            dungeonID = BeautifulSoup(res.text, 'lxml').find('input', attrs={'name' : 'dungeonId'})['value']

            for pos in posi_sequence:
                if res.text.find(f"startFight('{pos}', '{dungeonID}')") != -1: # Check if the button is present, so we don't spam pointless requests
                    if skip_boss and pos == max(posi_sequence):
                        # skip the last stage if skip_boss is True
                        self.driver.request('POST', settings.login_data['index_url'] + f"?mod=dungeon&loc={location}&action=cancelDungeon&sh={self.secureHash}", data = {'dungeonId': dungeonID})
                        #self.async_request('POST', settings.login_data['index_url'] + f"?mod=dungeon&loc={location}&action=cancelDungeon&sh={self.secureHash}", {'dungeonId': dungeonID})
                    else:
                        self.driver.request('POST', f"https://s{settings.login_data['server_number']}-{settings.login_data['server_country']}.gladiatus.gameforge.com/game/ajax/doDungeonFight.php" +
                                          f"?did={dungeonID}&posi={pos}&a={utility.get_milliseconds()}&sh={self.secureHash}")
                        #self.async_request('POST', f"https://s{settings.login_data['server_number']}-{settings.login_data['server_country']}.gladiatus.gameforge.com/game/ajax/doDungeonFight.php" +
                        #                   f"?did={dungeonID}&posi={pos}&a={utility.get_milliseconds()}&sh={self.secureHash}", {})
                    break

            print(f"We finished doing an action on {dungeon_name}!")
            return True
        except Exception as e:
            print(f"There was a a problem on {dungeon_name}: ", e)
            return False

    # Italy
    def go_dungeon_grimwood(self, difficulty = translation.dungeon_normal_text, skip_boss = False):
        return self.go_dungeon(location = 0, dungeon_name = f"Grimwood's dungeon ({translation.dungeon_grimwood_text})", posi_sequence = [1,3,5], difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_pirate_harbour(self, difficulty = translation.dungeon_normal_text, skip_boss = False):
        if difficulty == translation.dungeon_normal_text:
            return self.go_dungeon(location = 1, dungeon_name = f"Pirate Harbour's dungeon ({translation.dungeon_pirate_harbour_text})", posi_sequence = [1,2,3,8,7,6,5,4], difficulty = difficulty, skip_boss = skip_boss)
        if difficulty == translation.dungeon_advanced_text:
            return self.go_dungeon(location = 1, dungeon_name = f"Pirate Harbour's ADVANCED dungeon ({translation.dungeon_pirate_harbour_advanced_text})", posi_sequence = [1,2,3,4,5,6,7,8], difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_misty_mountains(self, difficulty = translation.dungeon_normal_text, skip_boss = False):
        if difficulty == translation.dungeon_normal_text:
            return self.go_dungeon(location = 2, dungeon_name = f"Misty Mountains' dungeon ({translation.dungeon_misty_mountains_text})", posi_sequence = [1,2,3,4], difficulty = difficulty, skip_boss = skip_boss)
        if difficulty == translation.dungeon_advanced_text:
            return self.go_dungeon(location = 2, dungeon_name = f"Misty Mountains' ADVANCED dungeon ({translation.dungeon_misty_mountains_advanced_text})", posi_sequence = [1,2,3,4], difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_wolf_cave(self, difficulty = translation.dungeon_normal_text, skip_boss = False):
        if difficulty == translation.dungeon_normal_text:
            return self.go_dungeon(location = 3, dungeon_name = f"Wolf Cave's dungeon ({translation.dungeon_wolf_cave_text})", posi_sequence = [1,2,3,4], difficulty = difficulty, skip_boss = skip_boss)
        if difficulty == translation.dungeon_advanced_text:
            return self.go_dungeon(location = 3, dungeon_name = f"Wolf Cave's ADVANCED dungeon ({translation.dungeon_wolf_cave_advanced_text})", posi_sequence = [1,2,3,4], difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_ancient_temple(self, difficulty = translation.dungeon_normal_text, skip_boss = False):
        return self.go_dungeon(location = 4, dungeon_name = f"Ancient temple's dungeon ({translation.dungeon_ancient_temple_text})", posi_sequence = [1,2,3,4,6,5], difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_barbarian_village(self, difficulty = translation.dungeon_normal_text, skip_boss = False):
        if difficulty == translation.dungeon_normal_text:
            return self.go_dungeon(location = 5, dungeon_name = f"Barbarian Village's dungeon ({translation.dungeon_barbarian_village_text})", posi_sequence = [1,2,3,4,5,6,7,8] , difficulty = difficulty, skip_boss = skip_boss)
        if difficulty == translation.dungeon_advanced_text:
            return self.go_dungeon(location = 5, dungeon_name = f"Barbarian Village's ADVANCED dungeon ({translation.dungeon_barbarian_village_advanced_text})", posi_sequence = [1,2,3,4,5,6,7,8,9,10] , difficulty = difficulty, skip_boss = skip_boss)

    # Africa
    def go_dungeon_voodoo_temple(self, difficulty = translation.dungeon_normal_text, skip_boss = False):
        return self.go_dungeon(location = 0, dungeon_name = f"Voodoo Temple's dungeon ({translation.dungeon_voodoo_temple_text})", posi_sequence = [1,2,4,5,6,7,8,3], difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_bridge(self, difficulty = translation.dungeon_normal_text, skip_boss = False):
        if difficulty == translation.dungeon_normal_text:
            return self.go_dungeon(location = 1, dungeon_name = f"Bridge's dungeon ({translation.dungeon_bridge_text})", posi_sequence = [1,2,3,4,5,6,7,8] , difficulty = difficulty, skip_boss = skip_boss)
        if difficulty == translation.dungeon_advanced_text:
            return self.go_dungeon(location = 1, dungeon_name = f"Bridge's ADVANCED dungeon ({translation.dungeon_bridge_advanced_text})", posi_sequence = [1,2,3,4,5,6,7,8,9,10] , difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_blood_cave(self, difficulty = translation.dungeon_normal_text, skip_boss = False):
        return self.go_dungeon(location = 2, dungeon_name = f"Blood Cave's dungeon ({translation.dungeon_blood_cave_text})", posi_sequence = [1,6,2,3,4] , difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_lost_harbour(self, difficulty = translation.dungeon_normal_text, skip_boss = False):
        if difficulty == translation.dungeon_normal_text:
            return self.go_dungeon(location = 3, dungeon_name = f"Lost Harbour's dungeon ({translation.dungeon_lost_harbour_text})", posi_sequence = [1,2,3,4,5,6,7,8,9] , difficulty = difficulty, skip_boss = skip_boss)
        if difficulty == translation.dungeon_advanced_text:
            return self.go_dungeon(location = 3, dungeon_name = f"Lost Harbour's ADVANCED dungeon ({translation.dungeon_lost_harbour_advanced_text})", posi_sequence = [1,2,3,4,5,6,7,8,9,10] , difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_umpokta_tribe(self, difficulty = translation.dungeon_normal_text, skip_boss = False):
        if difficulty == translation.dungeon_normal_text:
            return self.go_dungeon(location = 4, dungeon_name = f"Umpokta Tribe's dungeon ({translation.dungeon_umpokta_tribe_text})", posi_sequence = [1,2,3,4,5,6,7,8] , difficulty = difficulty, skip_boss = skip_boss)
        if difficulty == translation.dungeon_advanced_text:
            return self.go_dungeon(location = 4, dungeon_name = f"Umpokta Tribe's ADVANCED dungeon ({translation.dungeon_umpokta_tribe_advanced_text})", posi_sequence = [1,2,3,4,5,6,7] , difficulty = difficulty, skip_boss = skip_boss)

    # Germania
    def go_dungeon_cave_temple(self, difficulty = translation.dungeon_normal_text, skip_boss = False):
        return self.go_dungeon(location = 0, dungeon_name = f"Cave Temple's dungeon ({translation.dungeon_cave_temple_text})", posi_sequence = [1,2,3,4,5,6,7] , difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_green_forest(self, difficulty = translation.dungeon_normal_text, skip_boss = False):
        if difficulty == translation.dungeon_normal_text:
            return self.go_dungeon(location = 1, dungeon_name = f"The Green Forest's dungeon ({translation.dungeon_green_forest_text})", posi_sequence = [1,2,3,4,5,6,7] , difficulty = difficulty, skip_boss = skip_boss)
        if difficulty == translation.dungeon_advanced_text:
            return self.go_dungeon(location = 1, dungeon_name = f"The Green Forest's ADVANCED dungeon ({translation.dungeon_green_forest_advanced_text})", posi_sequence = [8,6,9,7] , difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_cursed_village(self, difficulty = translation.dungeon_normal_text, skip_boss = False):
        return self.go_dungeon(location = 2, dungeon_name = f"Cursed Village's dungeon ({translation.dungeon_green_forest_text})", posi_sequence = [1,2,3,4,5] , difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_death_hill(self, difficulty = translation.dungeon_normal_text, skip_boss = False):
        if difficulty == translation.dungeon_normal_text:
            return self.go_dungeon(location = 3, dungeon_name = f"Death Hill's dungeon ({translation.dungeon_death_hill_text})", posi_sequence = [1,2,3,4,5,4] , difficulty = difficulty, skip_boss = skip_boss)
