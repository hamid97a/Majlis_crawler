import sqlite3

#---------------------InitializeValue--------------------------

conn = sqlite3.connect("Update.db")
c = conn.cursor()
c.execute("""CREATE TABLE "Rules" (
	"Id"	INTEGER NOT NULL,
	"Title"	NVARCHAR(MAX),
	"approvalDate"	date,
	"announcementDate"	date,
	PRIMARY KEY("Id")
)""")
c.execute('''CREATE TABLE "approved" (
	"Id"	INTEGER NOT NULL,
	"appName"	NVARCHAR(500) NOT NULL,
	PRIMARY KEY("Id")
)''')
c.execute('''CREATE TABLE "Details" (
	"Id"	INTEGER NOT NULL,
	"Text"	NVARCHAR(MAX),
	"ApprovId"	INTEGER,
	"AnnouncementNumber"	NVARCHAR(100),
	"Article"	NVARCHAR(10),
	PRIMARY KEY("Id")
)''')
conn.commit()
conn.close()