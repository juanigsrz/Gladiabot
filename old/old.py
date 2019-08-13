"""
Testing
"""
def duplicateItems(type = 0, quality = -1, name = ""):
    print("Duplicating items")
    global x_place
    global y_place
    while True:
        millis1 = int(round(time.time() * 1000))
        """
        res = s.post(f'https://s28-en.gladiatus.gameforge.com/game/ajax.php',
                     data={'mod': 'inventory', 'submod': 'loadBag', 'bag': 513, 'shopType': 0, 'a': millis, #bag 514 pt inventar III, 513 pt II
                           'sh': secureHash})
                           """
        response = driver.request('POST', f'https://s28-en.gladiatus.gameforge.com/game/ajax.php', data={'mod': 'inventory', 'submod': 'loadBag', 'bag': 512, 'shopType': 0, 'a': millis, 'sh': secureHash}).text
        print("Response del bag 512: ")
        print(response)
        id = response.find("data-item-id=")
        id_item = ""
        if id != -1:
            while response[id] != '"':
                id += 1
            id += 1
            while response[id] != '"':
                id_item += response[id]
                id += 1
        i = 0
        for lol in range(x_place + (y_place - 1) * 8):
            i2 = response.find('-amount', i + 1)
            if i2 != -1:
                i = i2
        while response[i] != '"':
            i += 1
        i += 1
        print(response[i], response[i + 1], response[i + 2])
        if response[i] == '1' and response[i + 1] == '0' and response[i + 2] == '0':
            x_place += 1
        if x_place == 9 and y_place < 5:
            x_place = 1
            y_place += 1
        elif x_place == 9 and y_place == 5:
            return 0
        # s.post('https://s28-en.gladiatus.gameforge.com/game/ajax.php',
        #        data={'mod': 'forge', 'submod': 'rent', 'mode': 'smelting', 'slot': 0, 'rent': 2, 'item': id_item,
        #              'a': millis, 'sh': secureHash})
        """
        driver.request('POST', f'https://s28-en.gladiatus.gameforge.com/game/ajax.php',
                               data={'mod': 'forge', 'submod': 'rent', 'mode': 'smelting', 'slot': 0, 'rent': 2, 'item': id_item, 'a': millis, 'sh': secureHash})
                               """
        # s.post('https://s28-en.gladiatus.gameforge.com/game/ajax.php', data = {'mod':'forge','submod':'rent','mode':'workbench','slot':0,'rent':2,'item':id_item, 'a':millis, 'sh':secureHash})
        driver.request('POST', f'https://s28-en.gladiatus.gameforge.com/game/ajax.php', data = {'mod':'forge','submod':'rent','mode':'workbench','slot':0,'rent':2,'item':id_item, 'a':millis, 'sh':secureHash})

        for i in range(20):
            tl = threading.Thread(target=try_banclucru, args=(0,))
            t.append(tl)
        for i in range(20):
            t[i].start()
        # res = s.get(
        #     f'https://s28-en.gladiatus.gameforge.com/game/index.php?mod=packages&f={type}&fq={quality}&qry={name}&page=1&sh={secureHash}')
        response = driver.request('POST', f'https://s28-en.gladiatus.gameforge.com/game/index.php?mod=packages&f={type}&fq={quality}&qry={name}&page=1&sh={secureHash}').text
        i = response.find("are no packages") # "There are no packages"
        while i == -1:
            millis2 = int(round(time.time() * 1000))
            if millis2 - millis1 >= 15000:
                break
            # res = s.get(
            #     f'https://s28-en.gladiatus.gameforge.com/game/index.php?mod=packages&f={type}&fq={quality}&qry={name}&page=1&sh={secureHash}')
            response = driver.request('POST', f'https://s28-en.gladiatus.gameforge.com/game/index.php?mod=packages&f={type}&fq={quality}&qry={name}&page=1&sh={secureHash}').text
            i = response.find("are no packages")
            if i == -1:
                soup = BeautifulSoup(response, 'html5lib')
                supa = soup.find('input', attrs={'name': 'packages[]'})['value']
                # s.post(
                #     f'https://s28-en.gladiatus.gameforge.com/game/ajax.php?mod=inventory&submod=move&from=-{supa}&fromX=1&fromY=1&to=514&toX={x_place}&toY={y_place}&amount=1',
                #     data={'a': millis, 'sh': secureHash})
                driver.request('POST', f'https://s28-en.gladiatus.gameforge.com/game/ajax.php?mod=inventory&submod=move&from=-{supa}&fromX=1&fromY=1&to=514&toX={x_place}&toY={y_place}&amount=1'
                                     , data={'a': millis, 'sh': secureHash})

        t.clear()
        barrier.reset()
def try_workbench(x):
    global barrier
    barrier.wait()
    try:
        driver.request('POST', 'https://s28-en.gladiatus.gameforge.com/game/ajax.php', data={'mod': 'forge', 'submod': 'cancel', 'mode': 'workbench', 'slot': x, 'a': millis,
                         'sh': secureHash})
        print("Sent barrier try request")
    except:
        driver.request('POST', 'https://s28-en.gladiatus.gameforge.com/game/ajax.php', data={'mod': 'forge', 'submod': 'cancel', 'mode': 'workbench', 'slot': x, 'a': millis,
                     'sh': secureHash})
        print("Sent barrier except request")
    return 0
