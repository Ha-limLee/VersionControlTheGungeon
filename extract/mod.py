#This module is to be generalized

import requests
from bs4 import BeautifulSoup
import json
import sqlite3

def download(mod_id: str) -> None:
    url = 'https://modworkshop.net/mod/' + mod_id
    request_url = 'https://modworkshop.net/mws/api/modsapi.php'
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    #url = 'https://modworkshop.net/mws/api/modsapi.php?postcode=16078e8fcf6104e293ec3a688c7bb698&did=30815&fid=35579&func=download'

    res = soup.find('input', {'name' : 'postcode'})
    data = {}
    while res.name == 'input':
        data[res.get('name')] = res['value']
        res = res.find_next()
    response = requests.post(request_url, data=data)
    if response.status_code == 200:
        with open('test.zip', 'wb') as f:
            f.write(response.content)

def version(mod_id: str) -> str:
    """Get version of mod
    """
    url: str = 'https://modworkshop.net/mod/' + mod_id
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
 
    mod_text: str = soup.select_one('#mod_banner > div > div.d-flex.mt-auto.flex-column.flex-md-row > div.p-0.version.mt-auto > span').text
    res = mod_text.lstrip().split('|')[0]
    print(mod_id + ':' + res)

    return res

def search(mod_name: str) -> list[str]:
    url: str = 'https://modworkshop.net/mws/api/modsapi.php?cids[]=&tags[]=&sort=date&query=' + mod_name + '&gid=286&func=mods'
    req = requests.get(url)

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    py_data = json.loads(soup.text)

    res = [str]
    for elm in py_data['content']:
        print(elm['name'].strip())
        res.append(elm['name'].strip())

    return res

class _ModsDB:
    """
    Use ModsDB to create a instance instead of this class\n
    structure
        +---------------------------------+
        | mod_name | mod_id | mod_version |
        |---------------------------------|
        |                                 |
        +---------------------------------+
    """
    def __init__(self) -> None:
        self.__connection = sqlite3.connect('mod_versions.db')
        self.__cursor = self.__connection.cursor()
        self.__cursor.execute('CREATE TABLE IF NOT EXISTS mods\
            (name text, id text, version text)')
        pass

    def cleanup(self):
        print('clean up ModsDB')
        self.__connection.close()
        pass

    def insertDB(self, mod_name: str, mod_id: str, mod_version: str = '-1') -> None:
        self.__cursor.execute(f'INSERT INTO mods\
            VALUES({mod_name}, {mod_id}, {mod_version})')

class ModsDB:
    """
    ex)\n
    with ModsDB() as m:
        m.some_operation
    """
    def __enter__(self) -> _ModsDB:
        
        self.__ModsDB_obj = _ModsDB()
        print('ModsDB construct')
        return self.__ModsDB_obj

    def __exit__(self, exception_type, exception_value, traceback):
        print('ModsDB destruct')
        self.__ModsDB_obj.cleanup()

if __name__ == "__main__":
    #debug
    #version("30815")
    #search("King's")
    #createDB('gold', '333')
    with ModsDB() as m:
        m
'''
query_string = 'postcode', 'did', 'fid', 'func'
checked = 0
data = {}
for it in soup.select('div > form > input'):
    for param in query_string:
        if it['name'] == param:
            data[param] = it['value']
            break

response = requests.post(request_url, data=data)
if response.status_code == 200:
    with open('test.zip', 'wb') as f:
        f.write(response.content)
'''