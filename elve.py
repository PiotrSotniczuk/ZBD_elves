#!/usr/bin/python
from psycopg2 import connect, extensions, DatabaseError
from db_config import config
from mails_generator import get_mails

NR_OF_MAILS = 100

params = config()
conn = None
isolation = extensions.ISOLATION_LEVEL_READ_COMMITTED
mails = get_mails(NR_OF_MAILS)


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


# work
for mail in mails:
    try:
        conn = connect(**params)
        # conn.set_isolation_level(isolation)

        cur = conn.cursor()
        cur.execute("insert into pack(place, receiver) values (%s,%s) returning id;", (mail["country"], mail["name"]))
        pack_id = cur.fetchone()[0]

        if pack_treats(cur, mail, pack_id) == True:
            conn.commit()
        else:
            conn.rollback()

    except (Exception, DatabaseError) as error:
            print(error)
    finally:
            if conn is not None:
                conn.close()
