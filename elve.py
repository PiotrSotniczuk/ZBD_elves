#!/usr/bin/python
from psycopg2 import connect, extensions, DatabaseError
from db_config import config
from mails_generator import get_mails

NR_OF_MAILS = 10

params = config()
conn = None
isolation = extensions.ISOLATION_LEVEL_READ_COMMITTED
mails = get_mails(NR_OF_MAILS)

for mail in mails:

    try:
        conn = connect(**params)
        # conn.set_isolation_level(isolation)

        cur = conn.cursor()
        cur.execute("insert into pack(place, receiver) values (%s,%s) returning id;", (mail["country"], mail["name"]))
        pack_id = cur.fetchone()[0]

        for treat in mail['treats']:

            treat_name = treat[0]
            treat_nr = treat[1]
            cur.execute("select remaining from in_magazine where treat = %s;", [treat_name])
            remaining = cur.fetchone()[0]


            if(remaining < treat_nr):
                # search more rollback
                print(1)

            cur.execute("insert into in_pack values (%s,%s,%s);", (pack_id, treat_name, treat_nr))
            
            cur.execute("update in_magazine set remaining = remaining - %s where treat = %s;", (treat_nr, treat_name))


        conn.commit()

    except (Exception, DatabaseError) as error:
            print(error)
    finally:
            if conn is not None:
                conn.close()
