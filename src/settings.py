import os

"""
Global settings
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
