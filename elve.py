#!/usr/bin/python
from psycopg2 import connect, extensions, DatabaseError
from db_config import config
from mails_generator import get_mails
import sys
import time
from packing import pack_treats, pack_treats_sort_update_last

# argumnets 
NR_OF_MAILS = int(sys.argv[1])
SLEEP = int(sys.argv[2])

params = config()
conn = None

# READ_COMMITTED
# REPEATABLE_READ
# SERIALIZABLE
isolation = extensions.ISOLATION_LEVEL_READ_COMMITTED


# -------MAIN-----------

mails = get_mails(NR_OF_MAILS)
sucess = 0
fail = 0
retry = 0

# work
start = time.time()

for mail in mails:
    tries = 0
    while tries < 10:
        tries += 1
        try:
            conn = connect(**params)
            conn.set_isolation_level(isolation)

            cur = conn.cursor()
            cur.execute("insert into pack(place, receiver) values (%s,%s) returning id;", (mail["country"], mail["name"]))
            pack_id = cur.fetchone()[0]

            if pack_treats_sort_update_last(cur, mail, pack_id) == True:
                if(SLEEP > 0):
                    print("ZZZZZZ....")
                    time.sleep(SLEEP)
                conn.commit()
                sucess += 1
                break
            else:
                if(SLEEP > 0):
                    print("ZZZZZZ....")
                    time.sleep(SLEEP)
                conn.rollback()
                fail += 1
                break

        except (Exception, DatabaseError) as error:
                print(error)
                retry += 1
        finally:
            if conn is not None:
                conn.close()

print("--------ALL:",NR_OF_MAILS," (SUCC:", sucess, ", FAIL:", fail, ") RETRY:", retry, " SEK:", (time.time()-start),"----------")
