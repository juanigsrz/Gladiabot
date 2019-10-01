import os
import translation

"""
Global settings
"""
login_data = {
    'user_email'    : os.environ['user_email'],
    'user_password' : os.environ['user_password'],
    'login_url'     : 'https://lobby.gladiatus.gameforge.com/pt_BR/',
    'server_country': 'br',
    'server_number' : 36,
    'index_url'     : '',
    'ajax_url'      : '',
}
work_data = {'dollForJob7': 1, 'timeToWork': 1, 'jobType': 4}
food_data  = {'bag': 512} # 512 is the first inventory page, 513 is the second...

# Quests
quest_names = [ translation.circus_text, translation.arena_text, translation.enemies_anywhere_text, translation.find_items_text, "x Xamã" ]
quest_time_cycle = 20 # Seconds to wait until quests are checked again
