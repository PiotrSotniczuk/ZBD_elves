
# default packing
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


# packing after optimalization
def pack_treats_sort_update_last(cur, mail, pack_id):
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
        
        # write on list to update 
        to_update.append((treat_name, treat_nr))        

    # sort candies to update    
    to_update.sort()

    # update
    for tup in to_update:
        cur.execute("update in_magazine set remaining = remaining - %s where treat = %s;", (tup[1], tup[0]))
    
    return True
    