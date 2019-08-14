import time, os # System libraries
import arena, dungeon, expedition, inventory, quest, settings, utility, work # Local modules

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
