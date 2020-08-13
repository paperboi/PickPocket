from bs4 import BeautifulSoup
import time

from datetime import datetime
from notion.client import NotionClient

PATH_POCKET_FILE = "ril_export.html"
NOTION_TOKEN = "918be98b6ed238713209c761b1611d133ac2fcf5368e80fc7d0dd240de677ac2cfede6f2ba58c33915b72c2997106ef117b80e439be8a9386307625074ff8db1ef1f8f8f040f4d4d13d7699590ef"
NOTION_TABLE_ID = "https://www.notion.so/personaljeff/939537deaef5443bab2f7552fa3cd234?v=789809f8c63d4a5c9d4a6c0852e7db11"

class PocketListItem:
    title = ""
    url = ""
    tags = []
    addedOn = ""
    readStatus = None

    def __init__(self, title, url, tags, addedOn, readStatus):
        self.title = title
        self.url = url
        self.tags = tags
        self.addedOn = addedOn
        self.readStatus = readStatus

def retrieveAllPocketItems():
    with open(PATH_POCKET_FILE, encoding='utf8', errors='ignore') as fp:
        soup = BeautifulSoup(fp,'html.parser')
    allPocketListItems = []
    itemList = soup.h1.find_next("h1")

    # Retrieving the items from the user's Pocket List first.
    articles = itemList.find_all_previous("a")
    for eachItem in articles:
        title = eachItem.get_text()
        url = eachItem['href']
        tags = eachItem['tags'].split(',')
        addedOn = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(eachItem['time_added'])))
        readStatus = False
        eachPocketListItemData = PocketListItem(title,url,tags,addedOn,readStatus)
        allPocketListItems.append(eachPocketListItemData)

    # Retreiving the items from the user's Archive list next.
    articles = itemList.find_all_next("a")
    for eachItem in articles:
        title = eachItem.get_text()
        url = eachItem['href']
        tags = eachItem['tags'].split(',')
        addedOn = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(eachItem['time_added'])))
        # print(eachItem['time_added'])
        readStatus = True
        eachPocketListItemData = PocketListItem(title,url,tags,addedOn,readStatus)
        allPocketListItems.append(eachPocketListItemData)
    return allPocketListItems    

def itemAlreadyExists(item):
    index = 0
    for index, eachItem in enumerate(allPocketListItems):
        index += 1
        print(f"Checking for {eachItem.url}")
        if item.url == eachItem.url:
            print(True)
            return True
    print(False)
    return False

def addToNotion():
    client = NotionClient(token_v2=NOTION_TOKEN)
    cv = client.get_collection_view(NOTION_TABLE_ID)

    index = 0
    for index, eachItem in enumerate(allPocketListItems):
        if itemAlreadyExists(eachItem):
            continue
        index += 1
        row = cv.collection.add_row()
        print(row.get_property(vars))
        row.title = eachItem.title
        row.url = eachItem.url
        # row.tags = eachItem.tags
        # row.addedOn = eachItem.addedOn
        row.read = eachItem.readStatus
    #     print(f'{eachItem.tags}\n{eachItem.addedOn}')
    print(f"{index}/{len(allPocketListItems)} added")

print("Retreiving all items from Pocket")
allPocketListItems = retrieveAllPocketItems()
# retrieveAllPocketItems()
print("Retreival done")
print("Inserting items as table entries in Notion database")
addToNotion()
print("Transfer successfully completed")