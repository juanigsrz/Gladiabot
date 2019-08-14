
"""
General settings
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
sell_data  = {'bags': [513,]} # List of pages to be used to store and sell items



login_data['index_url'] = f"https://s{login_data['server_number']}-{login_data['server_country']}.gladiatus.gameforge.com/game/index.php"
login_data['ajax_url'] = f"https://s{login_data['server_number']}-{login_data['server_country']}.gladiatus.gameforge.com/game/ajax.php"
