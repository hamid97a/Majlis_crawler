from bs4 import BeautifulSoup
from requests_html import HTMLSession
from requests_html import HTML
import requests
import json
import time
from datetime import datetime
import re
import sqlite3
#---------------------InitializeValue--------------------------
#132299 in matnesh ajib gharibe

detailsList = []

def references(mosavab):
    for each in approvedList:
        if mosavab == each[1].strip():
            return(each[0])

def detailParse(det):
    return (det.full_text.strip().split(':'))[1].strip()

def fillDetails(spans):
    v = {'approvId':'','announcementNumber':'','article':''}
    for span in spans:
        if 'شماره ابلاغیه' in span.full_text:
            v['announcementNumber'] = detailParse(span)
        if 'ماده' in span.full_text:
            v['article'] = detailParse(span)
        if 'مرجع تصویب' in span.full_text:
            appname = detailParse(span)
            v['approvId'] = references(appname)
        else:
            pass
    return v

conn = sqlite3.connect('Pazhoohesh.db')
c= conn.cursor()
#select approved table for comparing approved names and save id in details tables
c.execute("SELECT * FROM approved")
approvedList = c.fetchall()
#select rules id for crawl text and details
c.execute("SELECT Id FROM Rules")
rows = c.fetchall()
i = 1
url = 'http://rc.majlis.ir/'
session = HTMLSession()
#
try:
    for row in rows:
        detailObj = {'Id':'','text':'','approvId':'','announcementNumber':'','article':''}
        #crawling text of rules
        ghanoon = session.get(url+"fa/law/print_version/"+str(row[0]),verify=False)
        matn = ghanoon.html.find('div[id="news-body"]',first=True).full_text.strip()
        details = session.get(url+"fa/law/show/"+str(row))
        spansList = details.html.find('div[class="sidebar-content"]',first=True)
        spans = spansList.find('span')
        s = fillDetails(spans)
        detailObj['Id'] = row[0]
        detailObj['text'] = matn
        detailObj['approvId'] = s['approvId']
        detailObj['announcementNumber'] = s['announcementNumber']
        detailObj['article'] = s['article']
        detailsList.append(tuple(detailObj.values()))
        if i % 20 == 0:
            c.executemany("INSERT INTO Details VALUES(?,?,?,?,?)",detailsList)
            conn.commit()
            detailsList = []
            print(i)
        if i % 300 == 0:
            time.sleep(30)
            session = HTMLSession()
        i+=1
except:
    print("except")
    v = open("Error.txt", "a")
    v.write(" # Details.py # We have except\n")
    v.close()

if detailsList != []:
    c.executemany("INSERT INTO Details VALUES(?,?,?,?,?)",detailsList)
    conn.commit()   
conn.close()