import time
import os

from selenium import webdriver
from seleniumrequests import Firefox
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup

"""
Global info
"""
login_data = {
    'user_email'    : os.environ['user_email'],
    'user_password' : os.environ['user_password'],
    'login_url'     : 'https://lobby.gladiatus.gameforge.com/en_GB/',
    'server_country': 'en',
    'server_number' : 28,
    'index_url'     : '',
    'ajax_url'      : '',
}
work_data = {'dollForJob7': 1, 'timeToWork': 1, 'jobType': 4}
food_data  = {'bag': 512} # 512 is the first inventory page, 513 is the second...
sell_data  = {'bags': [513,]}

"""
Utility
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

"""
Management
"""

def collect_food():
    # TODO: make sure the moved item is actually food
    # TODO: VERY slow, reduce the number of requests!
    print("Let's collect some food into the inventory!")
    try:
        for i in range(1,6):
            for j in range (1,9):
                res = driver.request('GET', login_data['index_url'] + f"?mod=packages&f=7&fq=-1&qry=&page=1&sh={secureHash}")
                soup = BeautifulSoup(res.text, 'html5lib')
                supa = soup.find('input', attrs={'name' : 'packages[]'})['value']
                driver.request('POST', login_data['ajax_url'] + f"?mod=inventory&submod=move&from=-{supa}&fromX=1&fromY=1&to={food_data['bag']}&toX={i}&toY={j}&amount=1&a={get_milliseconds()}&sh={secureHash}")
    except Exception as e:
        print("There was a problem when trying to collect food: ", e)
        return
    print("Finished collection food into the inventory!")
def collect_packages():
    pass
def sell_packages():
    pass
def eat_food():
    print("Let's go eat!")

    try:
        res = driver.request('POST', login_data['ajax_url'], data = {'mod': 'inventory', 'submod': 'loadBag', 'bag': food_data['bag'], 'shopType': 0, 'a': get_milliseconds(), 'sh': secureHash})

        i = res.text.find('&quot;Using: Heals')
        if i == -1:
            raise Exception('Found no food in the inventory')
        i2 = res.text.find('position-x', i)
        i3 = res.text.find('position-y', i)
        i2 += 12
        i3 += 12

        driver.request('POST', login_data['ajax_url'] + f"?mod=inventory&submod=move&from={food_data['bag']}&fromX=res.text[i2]&fromY=res.text[i3]&to=8&toX=1&toY=1&amount=1&doll=1&a={get_milliseconds()}&sh={secureHash})
        print("Finished eating!")
        return True
    except Exception as e:
        print("There was a problem on eat_food(): ", e)
        return False

"""
Work
"""
def go_work():
    print("Let's go to work!")
    try:
        response = driver.request('POST', login_data['index_url'] + f"?mod=work&submod=start&sh={secureHash}", data = work_data)
        work_soup = BeautifulSoup(response.text, 'html5lib')

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

"""
Quests
"""
def complete_quests():
    print("Let's complete quests!")
    try:
        while True:
            res = driver.request('GET', login_data['index_url'] + f"?mod=quests&sh=secureHash")
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

            driver.request('GET', login_data['index_url'] + f"?mod=quests&submod=finishQuest&questPos={nr}&sh=secureHash)
    except Exception as e:
        print("There was a a problem on complete_quests(): ", e)
        return
    print("Finished completing quests!")
def restart_quests():
    print("Let's restart quests!")
    try:
        while True:
            res = driver.request('GET', login_data['index_url'] + f"?mod=quests&sh=secureHash")
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

            driver.request('GET', login_data['index_url'] + f"?mod=quests&submod=restartQuest&questPos={nr}&sh=secureHash)
    except Exception as e:
        print("There was a a problem on restart_quests(): ", e)
        return
    print("Finished restarting quests!")
def accept_quests(names, skip_timed_quests = False):
    print("Let's accept quests!")

    try:
        res = driver.request('GET', login_data['index_url'] + f"?mod=quests&sh={secureHash})
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
                if res.text.find("slot_progress", i, i + 300) == -1:
                    # Quest not in progress
                    if skip_timed_quests and res.text.find("slot_time", i, i + 300) != -1:
                        # Quest has a timer
                        break
                    # TODO: find this value nicely
                    i += 9
                    nr = ''
                    nr += res.text[i]
                    try:
                        int(res.text[i + 1])
                        nr += res.text[i + 1]
                    except:
                        pass

                    driver.request('GET', login_data['index_url'] + f"?mod=quests&submod=startQuest&questPos={nr}&sh={secureHash})
                    print('Accepted a new quest!')
                    return True

    except Exception as e:
        print("There was a a problem on accept_quests(): ", e)
        return False

    # Couldn't find any relevant quests
    driver.request('GET', login_data['index_url'] + f"?mod=quests&submod=resetQuest&sh={secureHash})
    print("Couldn't find good quests, re-rolling")
    return False

"""
Expedition
"""
def go_expedition(location, stage):
    print("Let's go into an expedition!")

    try:
        res = driver.request('GET', login_data['ajax_url'] + f"?mod=location&submod=attack&location={location}&stage={stage}&premium=0&a={get_milliseconds()}&sh={secureHash})
    except Exception as e:
        print("There was a a problem on go_expedition(): ", e)
        return
    print("Finished going to the expedition!")

"""
Arena
"""
def go_arena():
    pass
def go_arena_provinciarum(max_fight_level = 9999):
    print("Let's go to the arena provinciarum!")

    try:
        res = driver.request('GET', login_data['index_url'] f"?mod=arena&submod=serverArena&aType=2&sh={secureHash})
        i2 = 0
        OK = 0
        i2 = res.text.find('Province</th')
        try:
            for x in range(5):
                i = res.text.find('<a target="_blank" href="', i2 + 50)
                i2 = res.text.find('<td>', i)
                # TODO: Find these values nicely
                nivel_oponent_temp = ""
                nivel_oponent_temp += res.text[i2 + 4]
                nivel_oponent_temp += res.text[i2 + 5]
                nivel_oponent = int(nivel_oponent_temp)
                if nivel_oponent < max_fight_level:
                    OK = 1
                    while res.text[i] != 'h' or res.text[i + 1] != 'r' or res.text [i + 2] != 'e' or res.text[i + 3] != 'f':
                        i += 1
                    i += 6
                    server = ""
                    while res.text[i] != 's' or res.text[i + 1] != ':' or res.text[i + 2] != '/' or res.text[i + 3] != '/' or res.text[i + 4] != 's':
                        i += 1
                    server += res.text[i + 5]
                    try:
                        vezi_daca_e_int = int(res.text[i + 6])
                        server += res.text[i + 6]
                    except:
                        pass
                    id_server = int(server)
                    i += 59
                    while res.text[i] != '=':
                        i += 1
                    i += 1
                    id_player_temp = ""
                    while res.text[i] != '"':
                        id_player_temp += res.text[i]
                        i += 1
                    id_player = int(id_player_temp)
                    driver.request('GET', login_data['ajax_url'] + f"?mod=arena&submod=doCombat&aType=2&opponentId={id_player}&serverId={id_server}&country={login_data['country']}&a={get_milliseconds()}&sh={secureHash})
                    print("Fighted in the arena provinciarum!")
                    break
            driver.request('POST', login_data['index_url'] + f"?mod=arena&submod=getNewOpponents&aType=2&sh={secureHash}, data = {'actionButton' : 'Search for opponents'})
        except Exception as e:
            print("There was a a problem when trying to fight in the arena provinciarum: ", e)
            return
    except Exception as e:
        print("There was a a problem on go_arena_provinciarum(): ", e)
        return
    print("Finished fighting in the arena provinciarum!")

"""
Circus
"""
def go_circus_turma():
    pass
def go_circus_provinciarum(max_fight_level = 9999):
    print("Let's go to circus provinciarum!")

    try:
        res = driver.request('GET', login_data['index_url'] + f"?mod=arena&submod=serverArena&aType=3&sh={secureHash})
        i2 = 0
        OK = 0
        i2 = res.text.find('Province</th')
        try:
            for x in range(5):
                i = res.text.find('<a target="_blank" href="', i2 + 50)
                i2 = res.text.find('<td>', i)
                # TODO: find these values nicely
                nivel_oponent_temp = ""
                nivel_oponent_temp += res.text[i2 + 4]
                nivel_oponent_temp += res.text[i2 + 5]
                nivel_oponent = int(nivel_oponent_temp)
                if nivel_oponent < max_fight_level:
                    OK = 1
                    while res.text[i] != 'h' or res.text[i + 1] != 'r' or res.text [i + 2] != 'e' or res.text[i + 3] != 'f':
                        i += 1
                    i += 6
                    server = ""
                    while res.text[i] != 's' or res.text[i + 1] != ':' or res.text[i + 2] != '/' or res.text[i + 3] != '/' or res.text[i + 4] != 's':
                        i += 1
                    server += res.text[i + 5]

                    try:
                        vezi_daca_e_int = int(res.text[i + 6])
                        server += res.text[i + 6]
                    except:
                        pass
                    id_server = int(server)
                    i += 59
                    while res.text[i] != '=':
                        i += 1
                    i += 1
                    id_player_temp = ""
                    while res.text[i] != '"':
                        id_player_temp += res.text[i]
                        i += 1
                    id_player = int(id_player_temp)
                    driver.request('GET', login_data['ajax_url'], data = {'mod': 'arena', 'submod': 'doCombat', 'aType': 3, 'opponentId': id_player, 'serverId': id_server, 'country': login_data["country"], 'a': get_milliseconds(), 'sh': secureHash})
                    print("Fighted in the circus provinciarum!")
                    break
            driver.request('POST', login_data['index_url'] + f"?mod=arena&submod=getNewOpponents&aType=3&sh={secureHash}", data = {'actionButton' : 'Search for opponents'})
        except Exception as e:
            print("There was a a problem when trying to fight in the circus provinciarum: ", e)
            return
    except Exception as e:
        print("There was a a problem on go_circus_provinciarum(): ", e)
        return
    print("Finished fighting in the circus provinciarum!")

"""
Main
"""
def plan_manager():
    """
    Defines the plan to play the game
    """
    print("I'm the plan manager!")

    while True:
        print("********** Starting new cycle **********")

        ### Manage HP
        hp_percent = get_hp_percentage()
        print(f"I have {hp_percent}% HP left")
        if hp_percent <= 45:
            print("I'm weak, i should eat something")
            if not eat_food():
                print("Couldn't eat, getting some food")
                collect_food()
                print("Trying to eat again")
                eat_food()

        ### Process quests
        complete_quests()
        restart_quests()
        accept_quests(names = ['The Dragon Stronghold',
                               'x Wild Boar',
                               'at expeditions, in dungeons or in the arenas',
                               'Circus Provinciarum',
                               'Provinciarum Arena',
                               ], skip_timed_quests = True)

        ### Fight in the arena
        go_arena_provinciarum()

        ### Fight in the circus
        go_circus_provinciarum()

        ### Go to expedition
        go_expedition(location = 3, stage = 1) # Wolf Cave - Wild Boar

        ### Go to dungeon
        go_dungeon_misty_mountains()

        ### Special event "On the Nile"
        # print("Special event (On the Nile): Figthing the goose")
        # driver.request('POST', login_data['ajax_url'] + f"?mod=location&submod=attack&location=nile_bank&stage=1&premium=0&a={get_milliseconds()}&sh={secureHash})

        ### Manage packages
        # collect_packages()

        ### Go to work
        time_working = go_work()
        if time_working != -1:
            print(f"Sleeping for {time_working} seconds...")
            time.sleep(time_working)
            print("Finished working!")

with Firefox() as driver:
    login_data['index_url'] = f"https://s{login_data['server_number']}-{login_data['server_country']}.gladiatus.gameforge.com/game/index.php"
    login_data['ajax_url'] = f"https://s{login_data['server_number']}-{login_data['server_country']}.gladiatus.gameforge.com/game/ajax.php"

    print("Logging in into Gladiatus")
    driver.get(login_data['login_url'])
    driver.find_element_by_id("loginRegisterTabs").find_element_by_css_selector('ul:nth-child(1)').find_element_by_css_selector('li:nth-child(1)').click()
    driver.find_element_by_xpath('//input[@name="email"]').send_keys(login_data['user_email'])
    driver.find_element_by_xpath('//input[@name="password"]').send_keys(login_data['user_password'])
    driver.find_element_by_xpath('//button[@type="submit"]').click()

    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('//span[@class="serverDetails"]')).click()
    driver.switch_to.window(driver.window_handles[1])

    time.sleep(20) # TODO: fix into an elegant solution, gotta wait for 'secureHash' in JS to be defined
    secureHash = get_hash(driver.page_source)

    print(f"Logged in, our secure hash is {secureHash}")
    plan_manager()
