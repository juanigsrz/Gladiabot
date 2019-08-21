import settings, utility

from abstract import AbstractManager

class ExpeditionManager(AbstractManager):
    """
    Expedition
    """
    def go_expedition(self, location, stage):
        print("Let's go into an expedition!")

        try:
            self.driver.request('POST', settings.login_data['ajax_url'] + f"?mod=location&submod=attack&location={location}&stage={stage}&premium=0&a={utility.get_milliseconds()}&sh={self.secureHash}")
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
            self.driver.request('POST', settings.login_data['index_url'] + f"?mod=dungeon&loc={location}&sh={self.secureHash}", data = {'dif1': difficulty})

            res = self.driver.request('GET', settings.login_data['index_url'] + f"?mod=dungeon&loc={location}&sh={self.secureHash}")
            # TODO: find this value nicely
            i = res.text.find('dungeonId')
            dungeonID = ""
            dungeonID += res.text[i + 18]
            dungeonID += res.text[i + 19]
            dungeonID += res.text[i + 20]
            dungeonID += res.text[i + 21]
            dungeonID += res.text[i + 22]
            dungeonID += res.text[i + 23]

            for pos in posi_sequence:
                if res.text.find(f"startFight('{pos}', '{dungeonID}')") != -1: # Check if the button is present, so we don't spam pointless requests
                    if skip_boss and pos == max(posi_sequence):
                        # skip the last stage if skip_boss is True
                        self.driver.request('POST', settings.login_data['index_url'] + f"?mod=dungeon&loc={location}&action=cancelDungeon&sh={self.secureHash}", data = {'dungeonId': dungeonID})
                    else:
                        self.driver.request('POST', f"https://s{settings.login_data['server_number']}-{settings.login_data['server_country']}.gladiatus.gameforge.com/game/ajax/doDungeonFight.php" +
                                          f"?did={dungeonID}&posi={pos}&a={utility.get_milliseconds()}&sh={self.secureHash}")
                    break

            print(f"We finished doing an action on {dungeon_name}!")
            return True
        except Exception as e:
            print(f"There was a a problem on {dungeon_name}: ", e)
            return False

    # Italy
    def go_dungeon_grimwood(self, difficulty = 'Normal', skip_boss = False):
        return self.go_dungeon(location = 0, dungeon_name = "Grimwood's dungeon (Gustavos Country House)", posi_sequence = [1,3,5], difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_pirate_harbour(self, difficulty = 'Normal', skip_boss = False):
        return self.go_dungeon(location = 1, dungeon_name = "Pirate Harbour's dungeon (On the run)", posi_sequence = [1,2,3,8,7,6], difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_misty_mountains(self, difficulty = 'Normal', skip_boss = False):
        return self.go_dungeon(location = 2, dungeon_name = "Misty Mountains' dungeon (The dragon stronghold)", posi_sequence = [1,2,3,4], difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_wolf_cave(self, difficulty = 'Normal', skip_boss = False):
        return self.go_dungeon(location = 3, dungeon_name = "Wolf Cave's dungeon (The cave of dark intrigue)", posi_sequence = [1,2,3,4], difficulty = difficulty, skip_boss = skip_boss)

    # Africa
    def go_dungeon_voodoo_temple(self, difficulty = 'Normal', skip_boss = False):
        return self.go_dungeon(location = 0, dungeon_name = "Voodoo Temple's dungeon (Temple of Perdition)", posi_sequence = [1,2,4,5,6,7,8], difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_bridge(self, difficulty = 'Normal', skip_boss = False):
        return self.go_dungeon(location = 1, dungeon_name = "Bridge's dungeon (Abducted)", posi_sequence = [1,2,3,4,5,6,7,8] , difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_blood_cave(self, difficulty = 'Normal', skip_boss = False):
        return self.go_dungeon(location = 2, dungeon_name = "Blood Cave's dungeon (Chamber of Pyro)", posi_sequence = [1,6,2,3,4] , difficulty = difficulty, skip_boss = skip_boss)
    def go_dungeon_lost_harbour(self, difficulty = 'Normal', skip_boss = False):
        return self.go_dungeon(location = 3, dungeon_name = "Lost Harbour's dungeon (Poisoned Country)", posi_sequence = [1,2,3,4,5,6,7,8,9] , difficulty = difficulty, skip_boss = skip_boss)

    # Germania
    def go_dungeon_cave_temple(self, difficulty = 'Normal', skip_boss = False):
        return self.go_dungeon(location = 0, dungeon_name = "Cave Temple's dungeon (Dark Catacombs)", posi_sequence = [1,2,3,4,5,6,7] , difficulty = difficulty, skip_boss = skip_boss)
