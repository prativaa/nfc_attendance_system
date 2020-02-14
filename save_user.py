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
clf = nfc.ContactlessFrontend("usb")
if clf.open("usb"):
    try:
        while True:
            print('PLACE CARD TO REGISTER')
            from nfc.clf import RemoteTarget
            target = clf.sense(RemoteTarget('106A'), RemoteTarget('106B'), RemoteTarget('212F'))
    
            tag = clf.connect(rdwr={ 'on-connect': lambda tag: False, 'iterations': 1, 'interval': 0.1, 'beep-on-connect': True})
    
            tag_uid = codecs.encode(tag.idm, 'hex').upper().decode('ASCII')
    
            sql_select_query = "SELECT id FROM users WHERE nfc_id = %s"
            cursor.execute(sql_select_query, (tag_uid,))
            cursor.fetchone()
    
            if cursor.rowcount >= 1:
                print("Overwrite existing user?")
                overwrite = raw_input("Overwite (Y/N)? ")
                if overwrite[0] == 'Y' or overwrite[0] == 'y':
                    print("Overwriting user...")
                    time.sleep(1)
                    sql_insert = "UPDATE users SET name = %s WHERE nfc_id=%s"
                elif overwrite[0] == 'N' or overwrite[0] == 'n':
                    print("You rejected to overwrite existing user")
                    continue
            else:
                sql_insert = "INSERT INTO users (name, nfc_id) VALUES (%s, %s)"
    
            print("-----TECHRISE-----")
            print("Enter Employee Details")
            new_name = raw_input("Employee Name: ")
            new_record = (new_name, tag_uid)
            cursor.execute(sql_insert, (new_name, tag_uid))
    
            db.commit()
            time.sleep(2) 
    except KeyboardInterrupt:
        pass
    finally:
        clf.close()