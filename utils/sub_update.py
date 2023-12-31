#!/usr/bin/env python3

from datetime import datetime
import json, re
import requests
from bs4 import BeautifulSoup


class update():
    def __init__(self,config={'list_file': './sub/sub_list.json'}):
        self.list_file = config['list_file']
        with open(self.list_file, 'r', encoding='utf-8') as f: # 载入订阅链接
            raw_list = json.load(f)
            self.raw_list = raw_list
        self.update_main()

    def url_updated(self,url): # 判断远程远程链接是否已经更新
        s = requests.Session()
        try:
            resp = s.get(url, timeout=2)
            status = resp.status_code
        except Exception:
            status = 404
        if status == 200:
            url_updated = True
        else:
            url_updated = False
        return url_updated

    def update_main(self):
        for sub in self.raw_list:
            id = sub['id']
            current_url = sub['url']
            try:
                if sub['update_method'] != 'auto' and sub['enabled'] == True:
                    print(f'Finding available update for ID{id}')
                    if sub['update_method'] == 'change_date':
                        new_url = self.change_date(id,current_url)
                        if new_url == current_url:
                            print(f'No available update for ID{id}\n')
                        else:
                            sub['url'] = new_url
                            print(f'ID{id} url updated to {new_url}\n')
                    elif sub['update_method'] == 'page_release':
                        new_url = self.find_link(id,current_url)
                        if new_url == current_url:
                            print(f'No available update for ID{id}\n')
                        else:
                            sub['url'] = new_url
                            print(f'ID{id} url updated to {new_url}\n')
            except KeyError:
                print(f'{id} Url not changed! Please define update method.')
            
            updated_list = json.dumps(self.raw_list, sort_keys=False, indent=2, ensure_ascii=False)
            file = open(self.list_file, 'w', encoding='utf-8')
            file.write(updated_list)
            file.close()

    def change_date(self,id,current_url):
        if id == 44:
            new_url = datetime.today().strftime('https://v2rayshare.com/wp-content/uploads/%Y/%m/%Y%m%d.txt')
        if id == 41:
            new_url = datetime.today().strftime('https://freenode.com/wp-content/uploads/%Y/%m/%m%d.txt')
        if id == 40:
            new_url = datetime.today().strftime('https://clashnode.com/wp-content/uploads/%Y/%m/%Y%m%d.txt')
        if id == 36:
            new_url = datetime.today().strftime('https://nodefree.org/dy/%Y/%m/%Y%m%d.txt')
        if id == 0:
            new_url = datetime.today().strftime('https://raw.githubusercontent.com/pojiezhiyuanjun/freev2/master/%m%d.txt')

        if self.url_updated(new_url):
            return new_url
        else:
            return current_url

    def find_link(self,id,current_url):
        if id == 38:
            try:
                res_json = requests.get('https://api.github.com/repos/mianfeifq/share/contents/').json()
                for file in res_json:
                    if file['name'].startswith('data'):
                        return file['download_url'] 
                else:
                    return current_url
            except Exception:
                return current_url
        if id == 33:
            url_update = 'https://v2cross.com/archives/1884'

            if self.url_updated(url_update):
                try:
                    resp = requests.get(url_update, timeout=5)
                    raw_content = resp.text

                    raw_content = raw_content.replace('amp;', '')
                    pattern = re.compile(r'https://shadowshare.v2cross.com/publicserver/servers/temp/\w{16}')
                    
                    new_url = re.findall(pattern, raw_content)[0]
                    return new_url
                except Exception:
                    return current_url
            else:
                return current_url
        if id == 41:
            try:
                url = "https://freenode.me/f/freenode"
                f = requests.get(url)
                soup = BeautifulSoup(f.content, features="html.parser")
                posts = soup.find("ul", {"class": "post-list"}).find_all("a")
                latest_release_url = posts[0]["href"]
                proxy_url = latest_release_url
                proxy_f = requests.get(proxy_url)
                proxy_soup = BeautifulSoup(proxy_f.content, features="html.parser")
                proxy_content = proxy_soup.find("div", {"class": "post-content-content"}).find_all(
                    "p"
                )
                for content in proxy_content:
                    new_url = content.string
                    if new_url is not None and "https://freenode.me/wp-content/uploads" in new_url:
                        return new_url
                return current_url
            except Exception:
                return current_url

if __name__ == '__main__':
    update()