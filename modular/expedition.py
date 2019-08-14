
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
