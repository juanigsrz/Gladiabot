import time, os, requests
import settings, utility

import asyncio, aiohttp

from abstract import AbstractManager
from bs4 import BeautifulSoup

from multiprocessing import Process, Semaphore, Value

class Barrier:
    def __init__(self, n):
        self.n       = n
        self.count   = Value('i', 0)
        self.mutex   = Semaphore(1)
        self.barrier = Semaphore(0)

    def wait(self):
        self.mutex.acquire()
        self.count.value += 1
        self.mutex.release()

        if self.count.value == self.n:
            self.barrier.release()

        self.barrier.acquire()
        self.barrier.release()

class HackManager(AbstractManager):
    def __init__(self, driver, secureHash, session):
        super().__init__(driver, secureHash)
        self.session = session
    def duplicate_items(self, simultaneous_attempts = 10):
        print("Duplicating items")

        while True:
            t = []
            self.barrier = Barrier(simultaneous_attempts)
            self.millis1 = int(round(time.time() * 1000))

            response = self.driver.request('POST', settings.login_data['ajax_url'], data = {'mod': 'inventory', 'submod': 'loadBag', 'bag': 513, 'shopType': 0, 'a': self.millis1, 'sh': self.secureHash}).text
            id = response.find("data-item-id=")
            id_item = ""
            if id != -1:
                while response[id] != '"':
                    id += 1
                id += 1
                while response[id] != '"':
                    id_item += response[id]
                    id += 1
            self.driver.request('POST', settings.login_data['ajax_url'], data = {'mod': 'forge', 'submod': 'rent', 'mode': 'workbench', 'slot': 0, 'rent': 2, 'item': id_item, 'a': self.millis1, 'sh': self.secureHash})

            for i in range(simultaneous_attempts):
                tl = Process(target=self.try_workbench, args=(0,))
                tl.daemon = True
                t.append(tl)
            for i in range(simultaneous_attempts):
                t[i].start()

            time.sleep(5)
    def try_workbench(self, x):
        self.barrier.wait()
        try:
            self.session.post(settings.login_data['ajax_url'], data = {'mod': 'forge', 'submod': 'cancel', 'mode': 'workbench', 'slot': x, 'a': self.millis1, 'sh': self.secureHash})
            print(f"PID: {os.getpid()} - Sent barrier try request")
            return True
        except:
            self.session.post(settings.login_data['ajax_url'], data = {'mod': 'forge', 'submod': 'cancel', 'mode': 'workbench', 'slot': x, 'a': self.millis1, 'sh': self.secureHash})
            print(f"PID: {os.getpid()} - 'Sent' barrier try EXCEPT request")
            return False
