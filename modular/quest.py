
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
