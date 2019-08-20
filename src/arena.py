import settings, utility

from abstract import AbstractManager

class ArenaManager(AbstractManager):
    """
    Arena
    """
    def go_arena(self):
        pass
    def go_arena_provinciarum(self, max_fight_level = 9999):
        print("Let's go to the arena provinciarum!")

        try:
            res = self.driver.request('GET', settings.login_data['index_url'] + f"?mod=arena&submod=serverArena&aType=2&sh={self.secureHash}")
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
                    if nivel_oponent <= max_fight_level:
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
                        self.driver.request('POST', settings.login_data['ajax_url'] + f"?mod=arena&submod=doCombat&aType=2&opponentId={id_player}&serverId={id_server}&country={settings.login_data['server_country']}&a={utility.get_milliseconds()}&sh={self.secureHash}")
                        print("Fighted in the arena provinciarum!")
                        break
                self.driver.request('POST', settings.login_data['index_url'] + f"?mod=arena&submod=getNewOpponents&aType=2&sh={self.secureHash}", data = {'actionButton' : 'Search+for+opponents'})
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
    def go_circus_turma(self):
        pass
    def go_circus_provinciarum(self, max_fight_level = 9999):
        print("Let's go to circus provinciarum!")

        try:
            res = self.driver.request('GET', settings.login_data['index_url'] + f"?mod=arena&submod=serverArena&aType=3&sh={self.secureHash}")
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
                    if nivel_oponent <= max_fight_level:
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
                        self.driver.request('POST', settings.login_data['ajax_url'] + f"?mod=arena&submod=doCombat&aType=3&opponentId={id_player}&serverId={id_server}&country={settings.login_data['server_country']}&a={utility.get_milliseconds()}&sh={self.secureHash}")
                        print("Fighted in the circus provinciarum!")
                        break
                self.driver.request('POST', settings.login_data['index_url'] + f"?mod=arena&submod=getNewOpponents&aType=3&sh={self.secureHash}", data = {'actionButton' : 'Search+for+opponents'})
            except Exception as e:
                print("There was a a problem when trying to fight in the circus provinciarum: ", e)
                return
        except Exception as e:
            print("There was a a problem on go_circus_provinciarum(): ", e)
            return
        print("Finished fighting in the circus provinciarum!")
