
"""
Dungeons
"""

def go_dungeon(location, dungeon_name, posi_sequence, difficulty):
    print(f"Let's go to {dungeon_name}!")

    try:
        driver.request('POST', login_data['index_url'] + f"?mod=dungeon&loc={location}&sh={secureHash}", data = {'dif1': difficulty})

        res = driver.request('GET', login_data['index_url'] + f"?mod=dungeon&loc={location}&sh=secureHash)
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
                driver.request('GET', f"https://s{login_data['server_number']}-{login_data['server_country']}.gladiatus.gameforge.com/game/ajax/doDungeonFight.php" +
                                      f"?did={dungeonID}&posi={pos}&a={get_milliseconds()}&sh=secureHash)
                break

        print(f"We finished doing an action on {dungeon_name}!")
        return True
    except Exception as e:
        print(f"There was a a problem on {dungeon_name}: ", e)
        return False

def go_dungeon_grimwood(difficulty = 'Normal'):
    return go_dungeon(location = 0, dungeon_name = "Grimwood's dungeon (Gustavo)", posi_sequence = [1,3,5], difficulty = difficulty)
def go_dungeon_pirate_harbour(difficulty = 'Normal'):
    return go_dungeon(location = 1, dungeon_name = "Pirate Harbour's dungeon (On the run)", posi_sequence = [1,2,3,8,7,6], difficulty = difficulty)
def go_dungeon_misty_mountains(difficulty = 'Normal'):
    return go_dungeon(location = 2, dungeon_name = "Misty Mountains' dungeon (The dragon stronghold)", posi_sequence = [1,2,3,4], difficulty = difficulty)
