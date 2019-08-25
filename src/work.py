import settings, utility

from abstract import AbstractManager
from bs4 import BeautifulSoup

class WorkManager(AbstractManager):
    """
    Work
    """
    def go_work(self):
        print("Let's go to work!")
        try:
            response = self.driver.request('POST', settings.login_data['index_url'] + f"?mod=work&submod=start&sh={self.secureHash}", data = settings.work_data)
            work_soup = BeautifulSoup(response.text, 'lxml')

            time_left = [item['data-ticker-time-left'] for item in work_soup.find_all('span', attrs={'data-ticker-time-left' : True})][0]
            time_working = int(time_left) / 1000 + 2

            print(f'Working for {time_working} seconds!')
            return time_working
        except Exception as e:
            print("Couldn't go to work with go_work()! Error: ", e)
            return -1
