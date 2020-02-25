import sqlite3

#---------------------InitializeValue--------------------------

conn = sqlite3.connect("Update.db")
c = conn.cursor()
c.execute("""CREATE TABLE "Rules" (
	"Id"	INTEGER NOT NULL,
	"Title"	TEXT,
	"approvalDate"	date,
	"announcementDate"	date,
	PRIMARY KEY("Id")
)""")
c.execute('''CREATE TABLE "approved" (
	"Id"	INTEGER NOT NULL,
	"appName"	TEXT NOT NULL,
	PRIMARY KEY("Id")
)''')
c.execute('''CREATE TABLE "Details" (
	"Id"	INTEGER NOT NULL,
	"Text"	TEXT,
	"ApprovId"	INTEGER,
	"AnnouncementNumber"	TEXT,
	"Article"	TEXT,
	PRIMARY KEY("Id")
)''')
conn.commit()
conn.close()