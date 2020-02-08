from bs4 import BeautifulSoup
from requests_html import HTMLSession
from requests_html import HTML
from datetime import datetime
import requests
import json
import time
import re
import sqlite3
#---------------------InitializeValue--------------------------
#crawling approve reference
#crawling table approved values (Id , appName)
url = 'http://rc.majlis.ir/'
session = HTMLSession()
conn = sqlite3.connect('Update.db')
c= conn.cursor()
references = []
i = 1
try:
    ghanoon = session.get(url+"fa/law/")
    refSelect = ghanoon.html.find('select[name="lu_approve_reference"]',first=True)
    refList = refSelect.find('option',first=False)
    while i < len(refList):
        refObj = {'id':'' ,'name':''}
        refObj['id'] = i
        refObj['name'] = refList[i].full_text.strip()
        references.append(tuple(refObj.values()))
        i+=1
    c.executemany("INSERT INTO approved VALUES(?,?)",references)
    conn.commit()
except:
    print("except")
    v = open("Error.txt", "a")
    v.write(" # FillReferences.py # We have except to crawl References "+str(datetime.now())+"\n")
    v.close()
conn.close()