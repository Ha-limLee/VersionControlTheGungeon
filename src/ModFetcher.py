import asyncio
from PySide6.QtWidgets import QApplication, QGridLayout, QWidget, QPushButton
import requests
from bs4 import BeautifulSoup
import sqlite3

from .ModResponse import ModResponse


class ModResponseContainer:
    def __init__(self):
        self.responses = []
        pass

    def getResponses(self):
        return self.responses
    



class ModFetcher:
    def __init__(self):
        self.responses: list[ModResponse] = None
        self.observers = []

    def addContainer(self, container: list):
        self.responses = container

    def addObserver(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)

    def notify(self, data):
        for each in self.observers:
            each.update(data)

    async def request(self, id: str):
        '''
        download something
        '''
        loop = asyncio.get_event_loop()

        url = 'https://modworkshop.net/mod/' + id

        future1 = loop.run_in_executor(None, requests.get, url)
        req = await future1
        
        # req = await loop.run_in_executor(None, requests.get(url))
        # req = requests.get(url)

        soup = BeautifulSoup(req.text, 'html.parser')

        res = soup.select_one('form.flex-grow.ml-2') # select download button

        if not res:
            return
        
        print(res['action']) # download button action

        request_url = 'https://modworkshop.net' + res['action']

        future2 = loop.run_in_executor(None, requests.post, request_url)
        response = await future2
        
        # response = await loop.run_in_executor(None, requests.post(request_url))
        # response = requests.post(request_url)

        if response.status_code == 200:
            self.responses.append(ModResponse(id, response))
            print(f'Got request of {id}')
        else:
            raise Exception(f'requesting {id} failed')

    async def _requestAll(self):
        # loop = asyncio.get_event_loop()
        
        conn = sqlite3.connect('versionTBL')
        cur = conn.cursor()
        ids = cur.execute('SELECT id FROM versionTBL')

        coroutines = [ self.request(id[0]) for id in ids ]
        
        await asyncio.gather(*coroutines)

        conn.close()
        self.notify(self.responses)

    def requestAll(self):
        asyncio.ensure_future(self._requestAll())
        # asyncio.create_task(self._requestAll(ids))

        '''
        for id in ids:
            try:
                asyncio.ensure_future(self.request(id[0]))
            except:
                pass
        '''
        

        '''
        for id in ids:
            try:
                loop.loop
                asyncio.run(self.request(id[0]))
                # self.request(id[0])
            except:
                pass
        '''

    '''
    def requestAll(self, ids):
        loop = asyncio.get_event_loop()
        loop.create_task(self._requestAll(ids))
        self.notify(self.responses)
    '''

class ModFetcherBtn(QWidget):
    def __init__(self):
        super().__init__()
        self.modFetcher = None
        self.observers = []
        self.btn = QPushButton('Fetch')

        layout = QGridLayout(self)
        layout.addWidget(self.btn)
        
        self.setLayout(layout)

        self.btn.clicked.connect(self.handleFetch)

    def addObserver(self, observer):
        if not observer in self.observers:
            self.observers.append(observer)

    def notify(self):
        for each in self.observers:
            each.update()

    def addModFetcher(self, modFetcher: ModFetcher):
        self.modFetcher = modFetcher
    
    def handleFetch(self):
        self.modFetcher.requestAll()
        

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    fetcherBtn = ModFetcherBtn()
    fetcher = ModFetcher()
    fetcherBtn.addModFetcher(fetcher)

    fetcherBtn.show()
    app.exec_()