from requests_html import HTMLSession
from requests_html import HTML
from datetime import datetime
from persiantools.jdatetime import JalaliDate
import requests
import json
import time
import re
import sqlite3
#---------------------InitializeValue--------------------------
#
#crawling table rules values (Id , Title , approvalDate , announcementDate)
url = 'http://rc.majlis.ir/'

page = 1
lastId = 0

#crawling rule table
session = HTMLSession()

def changeDate(mydate):
    if mydate != '':
        v = mydate.split('-')
        final = str(v[0])+"%2F"+str(v[1])+"%2F"+str(v[2])
        return (final)
    else:
        return(mydate)


#**************      date format example yyyy-mm-dd         ********************
#if you need all of rules input into dates empty string like ** fromDate = ''

fromDate = '1393-01-01'
toDate = '1398-12-02'

#*************************************
#*************************************
firstPage = session.get(url+"fa/law/search?page="+str(page)+"&from_app_date="+changeDate(fromDate)+"&to_app_date="+changeDate(toDate)+"&ot=d#aaa")
pageMax = int((firstPage.html.find('div[id="myTabContent"]>ul>li',first=True).full_text.strip().split(":"))[1])
if pageMax % 10 != 0:
    pageMax = (pageMax//10)+1
else:
    pageMax = pageMax//10

conn = sqlite3.connect('Update.db')
c= conn.cursor()
root = []

#********************************************Parsing
#*******************************************
def dateSplit(string):
    if string != '':
        s = string.split('/')
        if s[1].startswith('0'):
            s[1]=s[1][1:]
        if s[2].startswith('0'):
            s[2]=s[2][1:]
        tarikh =str(JalaliDate(int(s[0]), int(s[1]), int(s[2])).to_gregorian())
        return tarikh
    else:
        return string

def _multiple_replace(mapping, text):
    pattern = "|".join(map(re.escape, mapping.keys()))
    return re.sub(pattern, lambda m: mapping[m.group()], str(text))

def convert_fa_numbers(input_str):
    mapping = {
        '۰': '0',
        '۱': '1',
        '۲': '2',
        '۳': '3',
        '۴': '4',
        '۵': '5',
        '۶': '6',
        '۷': '7',
        '۸': '8',
        '۹': '9',
        '.': '.',
    }
    return _multiple_replace(mapping, input_str)
#********************************************
#****************************************

try:
    while page<=pageMax:
        try:
            lists = session.get(url+"fa/law/search?page="+str(page)+"&from_app_date="+changeDate(fromDate)+"&to_app_date="+changeDate(toDate)+"&ot=d#aaa")
        except:
            time.sleep(600)
            lists = session.get(url+"fa/law/search?page="+str(page)+"&from_app_date="+changeDate(fromDate)+"&to_app_date="+changeDate(toDate)+"&ot=d#aaa")
        table = lists.html.find('tbody',first=True)
        trList = table.find('tr')
        for each in trList:
            tdList = list(each.find('td'))
            rootobj = {'id':'' , 'title':'' , 'approvalDate':'' , 'announcementDate':'' }
            rootobj['id'] = int(tdList[0].full_text.strip())
            rootobj['title'] = convert_fa_numbers(tdList[1].full_text.strip())
            rootobj['approvalDate'] = dateSplit(tdList[2].full_text.strip())
            rootobj['announcementDate'] = dateSplit(tdList[3].full_text.strip())
            root.append(tuple(rootobj.values()))
            lastId = int(tdList[0].full_text.strip())
        if page % 20 == 0:
            c.executemany("INSERT INTO Rules VALUES(?,?,?,?)",root)
            conn.commit()
            root = []
        if page % 100 == 0:
            time.sleep(30)
            session = HTMLSession()
        if page % 1000 ==0:
            time.sleep(300)
        print(page)
        page +=1
except:
    print("except")
    v = open("Error.txt", "a")
    v.write(" # Pazhoohesh.py # In page : "+str(page) + " and id : "+str(lastId) +" we have except  "+str(datetime.now())+"\n")
    v.close()
    conn.close()

if root != []:
    c.executemany("INSERT INTO Rules VALUES(?,?,?,?)",root)
    conn.commit()   
conn.close()