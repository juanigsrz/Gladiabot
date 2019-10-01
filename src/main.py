import time, multiprocessing, threading, requests
import inventory, arena, utility, settings, work, expedition, player, quest, translation, hack

from random import randrange
from selenium import webdriver
from seleniumrequests import Firefox
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup

"""
Main
"""
def plan_manager():
    """
    Defines the plan to play the game
    """
    print("I'm the plan manager!")

    arenaManager      = arena.ArenaManager(driver, secureHash)
    playerManager     = player.PlayerManager(driver, secureHash)
    inventoryManager  = inventory.InventoryManager(driver, secureHash)
    questManager      = quest.QuestManager(driver, secureHash)
    workManager       = work.WorkManager(driver, secureHash)
    expeditionManager = expedition.ExpeditionManager(driver, secureHash)

    # questsProcess = multiprocessing.Process(target = questManager.loop_quests, args = (False,)) # skip_timed_quests = False
    questsProcess = threading.Thread(target = questManager.loop_quests, args = (False,)) # skip_timed_quests ?
    questsProcess.daemon = True # This process should die along with the main one
    questsProcess.start()

    while True:
        print("********** Starting new cycle **********")
        #playerManager.go_training(skills_to_train = ['Charisma', 'Intelligence'])

        ### Spend action points
        #if playerManager.is_circus_ready():
        arenaManager.go_circus_provinciarum()

        #if playerManager.is_dungeon_ready():
        expeditionManager.go_dungeon_umpokta_tribe(difficulty = translation.dungeon_advanced_text, skip_boss = False)

        hp_percent = playerManager.get_hp_percentage()
        if hp_percent <= 45:
            print("I'm weak, i should eat something")
            if not inventoryManager.eat_food():
                inventoryManager.collect_food()
                if not inventoryManager.eat_food():
                    print("Couldn't eat food :(, have none")
                    """
                    print("No food at all, going to work")
                    time_working = workManager.go_work()
                    if time_working != -1:
                        print(f"Working for {time_working} seconds...")
                        time.sleep(time_working)
                    """

        hp_percent = playerManager.get_hp_percentage()

        #if playerManager.is_expedition_ready():
        if hp_percent >= 45:
            expeditionManager.go_expedition(location = 7, stage = 3) # Xamã

        #if playerManager.is_arena_ready():
        if hp_percent >= 45:
            arenaManager.go_arena_provinciarum()

        ### Wait until next cycle
        time_working = settings.quest_time_cycle

        if time_working != -1:
            time_working = time_working + randrange(settings.quest_time_cycle)
            print(f"Sleeping for {time_working} seconds...")
            time.sleep(time_working)
            print("Finished sleeping!")

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

    time.sleep(15) # TODO: fix into an elegant solution, gotta wait for 'secureHash' in JS to be defined and set
    secureHash = utility.get_hash(driver.page_source)

    print(f"Logged in, our secure hash is {secureHash}")

    plan_manager()
