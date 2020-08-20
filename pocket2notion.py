import requests
from time import sleep
from bs4 import BeautifulSoup
from settings import PATH_POCKET_FILE, NOTION_TOKEN, NOTION_TABLE_ID

from random import choice
from uuid import uuid1

from datetime import datetime
from notion.client import NotionClient
from notion.collection import NotionDate

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
        if self.title == self.url:
            self._fetchTitleFromURL()
        self._addToNotion()
    
    def _fetchTitleFromURL(self):
        r = requests.get(self.url)
        sleep(1)
        soup = BeautifulSoup(r.content, 'lxml')
        self.title = soup.select_one('title').text
    
    def _addToNotion(self):
        row = cv.collection.add_row()
        row.title = self.title
        row.url = self.url
        self._setTag(row, 'prop', self.tags)
        row.added_on = NotionDate(datetime.fromtimestamp(self.addedOn))
        row.read = self.readStatus
        # print(f"{index}/{len(allPocketListItems)} added")

    def _addNewTag(self, schema, prop, tag):
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

    def _setTag(self, page, prop, new_values):
        schema = cv.collection.get("schema")
        new_values_set = set(new_values)

        if new_values == ['']:
            return []

        prop = next(
            (v for k, v in schema.items() if v["name"] == 'Tags'), None
        )

        if "options" not in prop: prop["options"] = []

        current_options_set = set(
            [o["value"] for o in prop["options"]]
        )
        intersection = new_values_set.intersection(current_options_set)

        if len(new_values_set) > len(intersection):
            difference = [v for v in new_values_set if v not in intersection]
            for d in difference:
                self._addNewTag(schema, prop, d)    
        page.set_property('Tags', new_values)

def itemAlreadyExists(itemURL):
    global allRows
    if allRows == []:
        return False
    for eachRow in allRows:
        if itemURL == eachRow.url:
            return True
    print(f"Adding {itemURL} to the list")
    return False

def retrieveAllPocketItems():
    with open(PATH_POCKET_FILE, encoding='utf8', errors='ignore') as fp:
        soup = BeautifulSoup(fp,'html.parser')
    itemList = soup.h1.find_next("h1")

    articles = itemList.find_all_previous("a")
    for eachItem in articles:
        if itemAlreadyExists(eachItem['href']):
            continue
        url = eachItem['href']
        title = eachItem.get_text()
        tags = eachItem['tags'].split(',')
        addedOn = int(eachItem['time_added'])
        readStatus = False
        PocketListItem(title,url,tags,addedOn,readStatus)

    # Retreiving the items from the user's Archive list next.
    articles = itemList.find_all_next("a")
    for eachItem in articles:
        if itemAlreadyExists(eachItem['href']):
            continue
        url = eachItem['href']
        title = eachItem.get_text()
        tags = eachItem['tags'].split(',')
        addedOn = int(eachItem['time_added'])
        readStatus = True
        PocketListItem(title,url,tags,addedOn,readStatus)

colors = ['default', 'gray', 'brown', 'orange', 'yellow', 'green', 'blue', 'purple', 'pink', 'red']

client = NotionClient(token_v2= NOTION_TOKEN)
cv = client.get_collection_view(NOTION_TABLE_ID)
allRows = cv.collection.get_rows()

print(cv.parent.views)

retrieveAllPocketItems()
print("Transfer successfully completed")