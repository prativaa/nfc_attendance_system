#!/usr/bin/env python
import time
import mysql.connector
import nfc
import codecs

db = mysql.connector.connect(
  host="",
  user="",
  passwd="",
  database=""
)

cursor = db.cursor()
while True:
    print('Place card to record attendance')
    
    clf = nfc.ContactlessFrontend("usb")
    from nfc.clf import RemoteTarget
    target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
    
    tag = clf.connect(rdwr={ 'on-connect': lambda tag: False, 'iterations': 1, 'interval': 0.1, 'beep-on-connect': True})
    
    tag_uid = codecs.encode(tag.idm, 'hex').upper().decode('ASCII')
    
    sql_select_query = "SELECT id, name FROM users WHERE nfc_id = %s"
    cursor.execute(sql_select_query, (tag_uid,))
    result = cursor.fetchone()
    
    if cursor.rowcount >= 1:
        print("Welcome " + result[1])
        cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],) )
        db.commit()
    else:
        print("User does not exist")
    time.sleep(2)
    clf.close()
        