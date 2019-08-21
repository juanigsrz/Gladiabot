import settings, utility

from abstract import AbstractManager
from bs4 import BeautifulSoup

class InventoryManager(AbstractManager):
    """
    Inventory management
    """
    def collect_food(self):
        # TODO: make sure the moved item is actually food
        # TODO: VERY slow, reduce the number of requests!
        print("Let's collect some food into the inventory!")
        try:
            """
            foodBagItems = self.driver.request('POST', settings.login_data['ajax_url'], # Items in the food_data['bag'] inventory bag
                                                data = {'mod': 'inventory', 'submod': 'loadBag', 'bag': settings.food_data['bag'], 'shopType': 0, 'a': utility.get_milliseconds(), 'sh': self.secureHash})
            foodPackages = self.driver.request('GET', settings.login_data['index_url'] + f"?mod=packages&f=7&fq=-1&qry=&page=1&sh={self.secureHash}") # Food packages

            inventory = [[True for x in range(6)] for y in range(9)]
            bagItems = BeautifulSoup(foodBagItems.text, 'lxml').findAll('div')
            for item in bagItems:

            packages = BeautifulSoup(foodBagItems.text, 'lxml').findAll(class = 'packa')
            for pack in packages:
                for i in range(1,6):
                    for j in range (1,9):
                        if inventory[i-1][j-1] == True:
                            inventory[i-1][j-1] = False
                            self.driver.request('POST', settings.login_data['ajax_url'] + f"?mod=inventory&submod=move&from=-{item['data-item-id']}&fromX=1&fromY=1&to={settings.food_data['bag']}&toX={i}&toY={j}&amount=1&a={utility.get_milliseconds()}&sh={self.secureHash}")
            """
            for i in range(1,6):
                for j in range (1,9):
                    res = self.driver.request('GET', settings.login_data['index_url'] + f"?mod=packages&f=7&fq=-1&qry=&page=1&sh={self.secureHash}")
                    soup = BeautifulSoup(res.text, 'lxml')
                    supa = soup.find('input', attrs={'name' : 'packages[]'})['value']
                    self.driver.request('POST', settings.login_data['ajax_url'] + f"?mod=inventory&submod=move&from=-{supa}&fromX=1&fromY=1&to={settings.food_data['bag']}&toX={i}&toY={j}&amount=1&a={utility.get_milliseconds()}&sh={self.secureHash}")
            print("Finished collecting food into the inventory!")
            return True
        except Exception as e:
            print("There was a problem when trying to collect food: ", e)
            return False
    def collect_packages(self):
        pass
    def sell_packages(self):
        pass
    def eat_food(self):
        print("Let's go eat!")
        try:
            res = self.driver.request('POST', settings.login_data['ajax_url'], data = {'mod': 'inventory', 'submod': 'loadBag', 'bag': settings.food_data['bag'], 'shopType': 0, 'a': utility.get_milliseconds(), 'sh': self.secureHash})

            i = res.text.find('&quot;Using: Heals')
            if i == -1:
                raise Exception('Found no food in the inventory')
            i2 = res.text.find('position-x', i)
            i3 = res.text.find('position-y', i)
            i2 += 12
            i3 += 12

            self.driver.request('POST', settings.login_data['ajax_url'] + f"?mod=inventory&submod=move&from={settings.food_data['bag']}&fromX={res.text[i2]}&fromY={res.text[i3]}&to=8&toX=1&toY=1&amount=1&doll=1&a={utility.get_milliseconds()}&sh={self.secureHash}")
            print("Finished eating!")
            return True
        except Exception as e:
            print("There was a problem on eat_food(): ", e)
            return False
