import aiohttp
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector
import asyncio
from urllib.parse import quote
from bs4 import BeautifulSoup

class Parser(object):
    async def get_films(self, page):
        lines = []
        pageUrl = "&start=" + str((page-1)*20)
        if page == 1:
            pageUrl = ""
        conn = ProxyConnector.from_url('socks5://195.2.74.75:9050')
        async with aiohttp.ClientSession(connector=conn) as session:
            async with session.get("http://nnmclub.to/forum/portal.php?c=10" + pageUrl) as resp:
                print ("http://nnmclub.to/forum/portal.php?c=10" + pageUrl)
                soup =  BeautifulSoup(await resp.read(), 'html.parser')
                for link in  soup.select('td[width="80%"] .pline'):
                    nameTor = ""
                    imageTor = ""
                    magnetTor = ""
                    razmerTor = ""
                    for name in link.select('.pgenmed'):
                        nameTor = name.text
                    for img in link.select('var'):
                        imageTor = img.get('title')
                    for raz in link.select('span.pcomm.bold'):
                        if "GB" in raz.text or "MB" in raz.text:
                            razmerTor = raz.text
                        

                    for url in link.select('a'):
                        if "magnet" in url.get('href'):
                            magnetTor = url.get('href')
                    if imageTor != "" and nameTor != "" and magnetTor!= "":
                        lines.append(nameTor + " : " + imageTor + " : " + magnetTor + ' : ' + razmerTor)
                return lines
    async def get_search(self, name):

        lines = []
        conn = ProxyConnector.from_url('socks5://195.2.74.75:9050')
        async with aiohttp.ClientSession(connector=conn) as session:
            payload = {'f': '-1', 'nm': quote(name), 'search_submit' : '%C8%F1%EA%E0%F2%FC'}
            print(payload)
            async with session.post("https://nnmclub.to/forum/tracker.php", data=payload) as resp:
                soup =  BeautifulSoup(await resp.read(), 'html.parser')
                
                for link in  soup.select('.genmed'):
                    nameTor = ""
                    linkTor = ""
                    for name in link.select('b'):
                        nameTor = name.text
                    for img in link.select('a'):
                        linkTor = img['href']
                        
                    print(nameTor)
                    
                    if  nameTor != "" and linkTor!= "":
                        lines.append(nameTor + " : " + linkTor)
                return lines
    
