from bs4 import BeautifulSoup
import time

from datetime import datetime
from notion.client import NotionClient
from notion.collection import NotionDate

PATH_POCKET_FILE = "ril_export.html"
NOTION_TOKEN = "918be98b6ed238713209c761b1611d133ac2fcf5368e80fc7d0dd240de677ac2cfede6f2ba58c33915b72c2997106ef117b80e439be8a9386307625074ff8db1ef1f8f8f040f4d4d13d7699590ef"
NOTION_TABLE_ID = "https://www.notion.so/personaljeff/0d2936c3aff9494db2fae6f8707a75d8?v=f282486e54904f95a6d12518a6e76b59"

client = NotionClient(token_v2=NOTION_TOKEN)
cv = client.get_collection_view(NOTION_TABLE_ID)
print(cv.parent.views)

class PocketListItem:
    title = ""
    url = ""
    tags = []
    addedOn = 0
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
        addedOn = int(eachItem['time_added'])
        readStatus = False
        eachPocketListItemData = PocketListItem(title,url,tags,addedOn,readStatus)
        allPocketListItems.append(eachPocketListItemData)

    # Retreiving the items from the user's Archive list next.
    articles = itemList.find_all_next("a")
    for eachItem in articles:
        title = eachItem.get_text()
        url = eachItem['href']
        tags = eachItem['tags'].split(',')
        addedOn = int(eachItem['time_added'])
        readStatus = True
        eachPocketListItemData = PocketListItem(title,url,tags,addedOn,readStatus)
        allPocketListItems.append(eachPocketListItemData)
    return allPocketListItems    

def itemAlreadyExists(item):
    index = 0
    for index, eachItem in enumerate(allPocketListItems):
        index += 1
        # print(f"Checking for {eachItem.url}")
        if item.url == eachItem.url:
            # print(True)
            return True
    # print(False)
    return False

from random import choice
from uuid import uuid1, uuid4
from pprintpp import pprint as pp

colors = ['default', 'gray', 'brown', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'red']

def addNewTag(cv, schema, prop, tag):
    dupe = next(
        (o for o in prop["options"] if o["value"] == tag), None
    )
    if dupe:
        raise ValueError(f'{tag} already exists in the schema!')

    prop["options"].append(
        {"id": str(uuid1()), "value": tag, "color": choice(colors)}
    )
    try:
        cv.collection.set("schema", schema)
    except (RecursionError, UnicodeEncodeError):
        pass

def setTag(page, cv, prop, new_values):
    schema = cv.collection.get("schema")
    new_values_set = set(new_values)

    if new_values == ['']:
        return []

    prop = next(
        (v for k, v in schema.items() if v["name"] == 'Tags'), None
    )

    if "options" not in prop: prop["options"] = []

    pp(prop)
    current_options_set = set(
        [o["value"] for o in prop["options"]]
    )
    intersection = new_values_set.intersection(current_options_set)

    if len(new_values_set) > len(intersection):
        difference = [v for v in new_values_set if v not in intersection]
        for d in difference:
            addNewTag(cv, schema, prop, d)    
    page.set_property('Tags', new_values)

def addToNotion():
    index = 0
    for index, eachItem in enumerate(allPocketListItems):
        if itemAlreadyExists(eachItem):
            continue
        index += 1
        row = cv.collection.add_row()
        row.title = eachItem.title
        row.url = eachItem.url
        setTag(row, cv, 'prop', eachItem.tags)
        row.added_on = NotionDate(datetime.fromtimestamp(eachItem.addedOn))
        pp(row.added_on)
        row.read = eachItem.readStatus
        # print(row.get_rows)
    print(f"{index}/{len(allPocketListItems)} added")

print("Retreiving all items from Pocket")
allPocketListItems = retrieveAllPocketItems()
print("Retreival done")
print("Inserting items as table entries in Notion database")
addToNotion()
print("Transfer successfully completed")