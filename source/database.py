import sqlite3

from threading import Thread
from queue import Queue

class DataBase(object):
    def __init__(self, name: str = "db") -> None:
        def init():
            self.connect = sqlite3.connect(name + ".sqlite")
            self.cursor = self.connect.cursor()

        def run():
            init()
            while True:
                item = self.queue.get()
                self.last_ans = self.__execute(item)
                self.is_get = False

        self.queue = Queue()
        self.thread = Thread(target=run)

        self.is_get = True
        self.last_ans = None

        self.thread.start()

    def __del__(self) -> None:
        self.connect.close()

    def execute(self, request: str):
        self.queue.put(request)
        return self.get()

    def get(self):
        if not self.is_get:
            return self.last_ans
            self.is_get = True

    def __execute(self, request: str):
        self.cursor.execute(request)
        self.connect.commit()
        return self.cursor.fetchall()
