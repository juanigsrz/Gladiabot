import time, enum
import arena, utility, settings

from selenium import webdriver
from seleniumrequests import Firefox
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup


"""
Inventory management
"""
def collect_food():
    # TODO: make sure the moved item is actually food
    # TODO: VERY slow, reduce the number of requests!
    print("Let's collect some food into the inventory!")
    try:
        for i in range(1,6):
            for j in range (1,9):
                res = driver.request('GET', settings.login_data['index_url'] + f"?mod=packages&f=7&fq=-1&qry=&page=1&sh={secureHash}")
                soup = BeautifulSoup(res.text, 'lxml')
                supa = soup.find('input', attrs={'name' : 'packages[]'})['value']
                driver.request('POST', settings.login_data['ajax_url'] + f"?mod=inventory&submod=move&from=-{supa}&fromX=1&fromY=1&to={settings.food_data['bag']}&toX={i}&toY={j}&amount=1&a={utility.get_milliseconds()}&sh={secureHash}")
    except Exception as e:
        print("There was a problem when trying to collect food: ", e)
        return
    print("Finished collecting food into the inventory!")
def collect_packages():
    pass
def sell_packages():
    pass
def eat_food():
    print("Let's go eat!")
    try:
        res = driver.request('POST', settings.login_data['ajax_url'], data = {'mod': 'inventory', 'submod': 'loadBag', 'bag': settings.food_data['bag'], 'shopType': 0, 'a': utility.get_milliseconds(), 'sh': secureHash})

        i = res.text.find('&quot;Using: Heals')
        if i == -1:
            raise Exception('Found no food in the inventory')
        i2 = res.text.find('position-x', i)
        i3 = res.text.find('position-y', i)
        i2 += 12
        i3 += 12

        driver.request('POST', settings.login_data['ajax_url'] + f"?mod=inventory&submod=move&from={settings.food_data['bag']}&fromX={res.text[i2]}&fromY={res.text[i3]}&to=8&toX=1&toY=1&amount=1&doll=1&a={utility.get_milliseconds()}&sh={secureHash}")
        print("Finished eating!")
        return True
    except Exception as e:
        print("There was a problem on eat_food(): ", e)
        return False
def purchase_gods_favours(god_to_purchase, favour_rank = 2):
    print("Let's try to purchase gods favours!")
    try:
        gods = enum.Enum('gods', ['Minerva', 'Diana', 'Vulcan', 'Mars', 'Apollo', 'Mercury'], start = 1)
        driver.request('POST', settings.login_data['index_url'] + f"?mod=gods&submod=activateBlessing&god={gods[god_to_purchase]}&rank={favour_rank}&sh={secureHash}")
        print(f"Finished trying purchasing {god_to_purchase}'s favours!")
    except Exception as e:
        print("There was a problem on purchase_gods_favours(): ", e)
    pass
def go_training(skill_to_train = 'Agility'):
    print("Let's go training!")
    try:
        skills = enum.Enum('skills', ['Strength', 'Dexterity', 'Agility', 'Constitution', 'Charisma', 'Intelligence'], start = 1)
        driver.request('POST', settings.login_data['index_url'] + f"?mod=training&submod=train&skillToTrain={skills[skill_to_train]}&sh={secureHash}")
        print(f"Tried to train '{skill_to_train}' successfully!")
    except Exception as e:
        print("Couldn't train in go_training()! Error: ", e)


"""
Work
"""
def go_work():
    print("Let's go to work!")
    try:
        response = driver.request('POST', settings.login_data['index_url'] + f"?mod=work&submod=start&sh={secureHash}", data = settings.work_data)
        work_soup = BeautifulSoup(response.text, 'lxml')

        time_left = [item['data-ticker-time-left'] for item in work_soup.find_all('span', attrs={'data-ticker-time-left' : True})][0]
        time_working = int(time_left) / 1000 + 2

        print(f'Working for {time_working} seconds!')
        return time_working
    except Exception as e:
        print("Couldn't go to work with go_work()! Error: ", e)
        return -1

"""
Dungeons
"""
def go_dungeon(location, dungeon_name, posi_sequence, difficulty, skip_boss):
    print(f"Let's go to {dungeon_name}!")

    try:
        driver.request('POST', settings.login_data['index_url'] + f"?mod=dungeon&loc={location}&sh={secureHash}", data = {'dif1': difficulty})

        res = driver.request('GET', settings.login_data['index_url'] + f"?mod=dungeon&loc={location}&sh={secureHash}")
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
                    driver.request('POST', settings.login_data['index_url'] + f"?mod=dungeon&loc={location}&action=cancelDungeon&sh={secureHash}", data = {'dungeonId': dungeonID})
                else:
                    driver.request('POST', f"https://s{settings.login_data['server_number']}-{settings.login_data['server_country']}.gladiatus.gameforge.com/game/ajax/doDungeonFight.php" +
                                      f"?did={dungeonID}&posi={pos}&a={utility.get_milliseconds()}&sh={secureHash}")
                break

        print(f"We finished doing an action on {dungeon_name}!")
        return True
    except Exception as e:
        print(f"There was a a problem on {dungeon_name}: ", e)
        return False

# Italy
def go_dungeon_grimwood(difficulty = 'Normal', skip_boss = False):
    return go_dungeon(location = 0, dungeon_name = "Grimwood's dungeon (Gustavos Country House)", posi_sequence = [1,3,5], difficulty = difficulty, skip_boss = skip_boss)
def go_dungeon_pirate_harbour(difficulty = 'Normal', skip_boss = False):
    return go_dungeon(location = 1, dungeon_name = "Pirate Harbour's dungeon (On the run)", posi_sequence = [1,2,3,8,7,6], difficulty = difficulty, skip_boss = skip_boss)
def go_dungeon_misty_mountains(difficulty = 'Normal', skip_boss = False):
    return go_dungeon(location = 2, dungeon_name = "Misty Mountains' dungeon (The dragon stronghold)", posi_sequence = [1,2,3,4], difficulty = difficulty, skip_boss = skip_boss)
def go_dungeon_wolf_cave(difficulty = 'Normal', skip_boss = False):
    return go_dungeon(location = 3, dungeon_name = "Wolf Cave's dungeon (The cave of dark intrigue)", posi_sequence = [1,2,3,4], difficulty = difficulty, skip_boss = skip_boss)

# Africa
def go_dungeon_voodoo_temple(difficulty = 'Normal', skip_boss = False):
    return go_dungeon(location = 0, dungeon_name = "Voodoo Temple's dungeon (Temple of Perdition)", posi_sequence = [1,2,4,5,6,7,8], difficulty = difficulty, skip_boss = skip_boss)
def go_dungeon_bridge(difficulty = 'Normal', skip_boss = False):
    return go_dungeon(location = 1, dungeon_name = "Bridge's dungeon (Abducted)", posi_sequence = [1,2,3,4,5,6,7,8] , difficulty = difficulty, skip_boss = skip_boss)
def go_dungeon_blood_cave(difficulty = 'Normal', skip_boss = False):
    return go_dungeon(location = 2, dungeon_name = "Blood Cave's dungeon (Chamber of Pyro)", posi_sequence = [1,6,2,3,4] , difficulty = difficulty, skip_boss = skip_boss)
def go_dungeon_lost_harbour(difficulty = 'Normal', skip_boss = False):
    return go_dungeon(location = 3, dungeon_name = "Lost Harbour's dungeon (Poisoned Country)", posi_sequence = [1,2,3,4,5,6,7,8,9] , difficulty = difficulty, skip_boss = skip_boss)

# Germania
def go_dungeon_cave_temple(difficulty = 'Normal', skip_boss = False):
    return go_dungeon(location = 0, dungeon_name = "Cave Temple's dungeon (Dark Catacombs)", posi_sequence = [1,2,3,4,5,6,7] , difficulty = difficulty, skip_boss = skip_boss)

"""
Quests
"""
def process_quests(names, skip_timed_quests = False):
    print("Let's process quests!")
    complete_quests()
    restart_quests()
    return accept_quests(names = names, skip_timed_quests = skip_timed_quests)
def complete_quests():
    print("Let's complete quests!")
    try:
        while True:
            res = driver.request('GET', settings.login_data['index_url'] + f"?mod=quests&sh={secureHash}")
            i = res.text.find('button_finish')
            if i == -1:
                break
            i = res.text.find('questPos', i)
            # TODO: find this value nicely
            if i != -1:
                i += 9
            nr = ''
            nr += res.text[i]
            try:
                int(res.text[i + 1])
                nr += res.text[i + 1]
            except:
                pass

            driver.request('GET', settings.login_data['index_url'] + f"?mod=quests&submod=finishQuest&questPos={nr}&sh={secureHash}")
    except Exception as e:
        print("There was a a problem on complete_quests(): ", e)
        return
    print("Finished completing quests!")
def restart_quests():
    print("Let's restart quests!")
    try:
        while True:
            res = driver.request('GET', settings.login_data['index_url'] + f"?mod=quests&sh={secureHash}")
            i = res.text.find('button_restart')
            if i == -1:
                break
            i = res.text.find('questPos', i)
            # TODO: find this value nicely
            if i != -1:
                i += 9
            nr = ''
            nr += res.text[i]
            try:
                int(res.text[i + 1])
                nr += res.text[i + 1]
            except:
                pass

            driver.request('GET', settings.login_data['index_url'] + f"?mod=quests&submod=restartQuest&questPos={nr}&sh={secureHash}")
    except Exception as e:
        print("There was a a problem on restart_quests(): ", e)
        return
    print("Finished restarting quests!")
def accept_quests(names, skip_timed_quests):
    print("Let's accept quests!")
    try:
        res = driver.request('GET', settings.login_data['index_url'] + f"?mod=quests&sh={secureHash}")
        pos = res.text.find("Accepted quests:")
        pos += 17
        if res.text[pos] == res.text[pos+4]:
            print("We got no slots to accept more quests")
            return False
        for name in names:
            i = pos
            while True:
                i = res.text.find(name, i)
                i = res.text.find("questPos", i)
                if i == -1:
                    break
                if res.text.find("slot_progress", i, i + 200) == -1:
                    # Quest not in progress
                    i += 9
                    if skip_timed_quests and res.text.find("slot_time", i, i + 300) != -1:
                        # Quest has a timer
                        continue
                    # TODO: find this value nicely
                    nr = ''
                    nr += res.text[i]
                    try:
                        int(res.text[i + 1])
                        nr += res.text[i + 1]
                    except:
                        pass

                    driver.request('GET', settings.login_data['index_url'] + f"?mod=quests&submod=startQuest&questPos={nr}&sh={secureHash}")
                    print('Accepted a new quest!')
                    return True

    except Exception as e:
        print("There was a a problem on accept_quests(): ", e)
        return False

    # Couldn't find any relevant quests
    driver.request('GET', settings.login_data['index_url'] + f"?mod=quests&submod=resetQuests&sh={secureHash}")
    print("Couldn't find good quests, re-rolling")
    return False

"""
Expedition
"""
def go_expedition(location, stage):
    print("Let's go into an expedition!")

    try:
        driver.request('POST', settings.login_data['ajax_url'] + f"?mod=location&submod=attack&location={location}&stage={stage}&premium=0&a={utility.get_milliseconds()}&sh={secureHash}")
    except Exception as e:
        print("There was a a problem on go_expedition(): ", e)
        return
    print("Finished going to the expedition!")


"""
Main
"""
def plan_manager():
    """
    Defines the plan to play the game
    """
    print("I'm the plan manager!")

    quest_names = [ 'Arena', 'Circus' ]

    """
    quest_names = [ 'Circus Provinciarum', 'Provinciarum Arena', 'Abducted:', 'Lost Harbour: Defeat 6 opponents of your choice', 'x Giant Water Snake',
                    'at expeditions, in dungeons or in the arenas', 'hours as a Butcher', ]
    """

    arenaManager = arena.ArenaManager(driver, secureHash)

    while True:
        print("********** Starting new cycle **********")

        ### Manage HP
        hp_percent = arenaManager.get_hp_percentage()
        print(f"I have {hp_percent}% HP left")
        if hp_percent <= 50:
            print("I'm weak, i should eat something")
            if not eat_food():
                print("Couldn't eat, getting some food")
                collect_food()
                print("Trying to eat again")
                eat_food()

        ### Check quests
        process_quests(names = quest_names, skip_timed_quests = False)

        ### Fight in the arenas
        arenaManager.go_arena_provinciarum(max_fight_level = 46)
        arenaManager.go_circus_provinciarum(max_fight_level = 40)

        ### Go to expedition
        go_expedition(location = 0, stage = 3) # Cave Temple - Centurion

        ### Go to dungeon
        go_dungeon_cave_temple(difficulty = 'Normal', skip_boss = True)

        ### Special event "On the Nile"
        # print("Special event (On the Nile): Figthing the goose")
        # driver.request('POST', settings.login_data['ajax_url'] + f"?mod=location&submod=attack&location=nile_bank&stage=1&premium=0&a={utility.get_milliseconds()}&sh={secureHash}")

        ### Manage packages
        # collect_packages()
        # sell_packages()

        ### Check quests again after figthing
        process_quests(names = quest_names, skip_timed_quests = False)

        ### Go to work
        time_working = 3 * 60 # go_work()
        if time_working != -1:
            print(f"Sleeping for {time_working} seconds...")
            time.sleep(time_working)
            print("Finished working!")

with Firefox() as driver:
    settings.login_data['index_url'] = f"https://s{settings.login_data['server_number']}-{settings.login_data['server_country']}.gladiatus.gameforge.com/game/index.php"
    settings.login_data['ajax_url'] = f"https://s{settings.login_data['server_number']}-{settings.login_data['server_country']}.gladiatus.gameforge.com/game/ajax.php"

    print("Logging in into Gladiatus")
    """
    # Block image loading on Firefox
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    driver = Firefox(firefox_profile=firefox_profile)
    """

    driver.get(settings.login_data['login_url'])
    driver.find_element_by_id("loginRegisterTabs").find_element_by_css_selector('ul:nth-child(1)').find_element_by_css_selector('li:nth-child(1)').click()
    driver.find_element_by_xpath('//input[@name="email"]').send_keys(settings.login_data['user_email'])
    driver.find_element_by_xpath('//input[@name="password"]').send_keys(settings.login_data['user_password'])
    driver.find_element_by_xpath('//button[@type="submit"]').click()

    play_button = WebDriverWait(driver, 15).until(lambda x: x.find_element_by_xpath('//span[@class="serverDetails"]'))
    play_button.click()
    driver.switch_to.window(driver.window_handles[1])

    time.sleep(15) # TODO: fix into an elegant solution, gotta wait for 'secureHash' in JS to be defined
    secureHash = utility.get_hash(driver.page_source)

    print(f"Logged in, our secure hash is {secureHash}")
    plan_manager()
