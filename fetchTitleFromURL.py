import requests
from time import sleep
from bs4 import BeautifulSoup

def fetchTitleFromURL(url):
    session = requests.Session()
    r = session.get(url)
    sleep(1)
    soup = BeautifulSoup(r.content, 'lxml')
    title = soup.select_one('title').text
    return(title)