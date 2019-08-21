import threading
import settings, utility

from bs4 import BeautifulSoup

class AbstractManager():
    def __init__(self, driver, secureHash):
        self.driver, self.secureHash = driver, secureHash

    def async_request(self, request_type, url, data):
        t = threading.Thread(target = self.driver.request, args = (request_type, url, data,))
        t.daemon = True
        t.start()
