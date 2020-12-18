#!/usr/bin/python
from psycopg2 import connect, extensions, DatabaseError
from db_config import config
from mails_generator import get_mails
import sys
import time

NR_OF_MAILS = int(sys.argv[1])

params = config()
conn = None
isolation = extensions.ISOLATION_LEVEL_READ_COMMITTED


def pack_treats(cur, mail, pack_id):
    for treat in mail['treats']:

        treat_name = treat[0]
        treat_nr = treat[1]
        cur.execute("select remaining from in_magazine where treat = %s;", [treat_name])
        remaining = cur.fetchone()[0]

        if remaining < treat_nr:
            cur.execute("select * from similar_treat where treat_1=%s or treat_2=%s order by similarity desc;", (treat_name, treat_name))
            
            rows = cur.fetchall()
            found = False

            if rows is None:
                return False
            
            for row in rows:
                replacement = row[0]
                if row[0] == treat_name:
                    replacement = row[1]
                
                cur.execute("select remaining from in_magazine where treat = %s;", [replacement])
                remaining = cur.fetchone()[0]
                if remaining >= treat_nr:
                    found = True
                    treat_name = replacement
                    break

            if(found == False):
                return False
        
        cur.execute("insert into in_pack values (%s,%s,%s);", (pack_id, treat_name, treat_nr))        
        cur.execute("update in_magazine set remaining = remaining - %s where treat = %s;", (treat_nr, treat_name))

    return True

def pack_treats_update_last(cur, mail, pack_id):
    to_update = []
    for treat in mail['treats']:

        treat_name = treat[0]
        treat_nr = treat[1]
        cur.execute("select remaining from in_magazine where treat = %s;", [treat_name])
        remaining = cur.fetchone()[0]

        if remaining < treat_nr:
            cur.execute("select * from similar_treat where treat_1=%s or treat_2=%s order by similarity desc;", (treat_name, treat_name))
            
            rows = cur.fetchall()
            found = False

            if rows is None:
                return False
            
            for row in rows:
                replacement = row[0]
                if row[0] == treat_name:
                    replacement = row[1]
                
                cur.execute("select remaining from in_magazine where treat = %s;", [replacement])
                remaining = cur.fetchone()[0]
                if remaining >= treat_nr:
                    found = True
                    treat_name = replacement
                    break

            if(found == False):
                return False
        
        cur.execute("insert into in_pack values (%s,%s,%s);", (pack_id, treat_name, treat_nr))

        to_update.append((treat_nr, treat_name))        
        
    for tup in to_update:
        cur.execute("update in_magazine set remaining = remaining - %s where treat = %s;", (tup[0], tup[1]))
    
    return True



# -------MAIN-----------

mails = get_mails(NR_OF_MAILS)
sucess = 0
fail = 0
er = 0

# work
start = time.time()

for mail in mails:
    try:
        conn = connect(**params)
        # conn.set_isolation_level(isolation)

        cur = conn.cursor()
        cur.execute("insert into pack(place, receiver) values (%s,%s) returning id;", (mail["country"], mail["name"]))
        pack_id = cur.fetchone()[0]

        if pack_treats_update_last(cur, mail, pack_id) == True:
            conn.commit()
            sucess += 1
        else:
            conn.rollback()
            fail += 1

    except (Exception, DatabaseError) as error:
            print(error)
            er += 1
    finally:
            if conn is not None:
                conn.close()

print("--------SUCC:", sucess, " FAIL:", fail, " ER:", er, " NR/SEK:", NR_OF_MAILS/(time.time()-start),"----------")