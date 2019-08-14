
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
