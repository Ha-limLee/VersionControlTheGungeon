#This module is to be generalized

import requests
from bs4 import BeautifulSoup

def download():
    url = 'https://modworkshop.net/mod/30815'
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

def version(mod_id:str)->str:
    url:str = 'https://modworkshop.net/mod/' + mod_id
    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
 
    res = soup.select_one('#mod_banner > div > div.d-flex.mt-auto.flex-column.flex-md-row > div.p-0.version.mt-auto > span').text
    print(res)

    return res

if __name__ == "__main__":
    version("30815")
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