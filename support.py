import sqlite3,requests,json
from datetime import datetime
from dbconnect import get_db_connection as connecting



# con = connecting()
# con.row_factory = sqlite3.Row  
# cur = con.cursor()

# con.execute('DELETE FROM packageId')
# con.commit()
 


def refresh():

    print("#"*1000)
    print("in refresh")
    print("#"*1000)
    ref = {'test':'1'}
    url = "https://affise.c2a.in/app_working_link.php?fetch_campaigns=List+Campaigns"
    res = requests.get(url)
    t = json.loads(res.text)
    lis = t.get('suggestedApps')

    con = connecting()
    try:
        # con = sqlite3.connect("working.db")  

        con.execute('DELETE FROM workinglinks')
        con.commit()
    except:
        pass
    insert_rows = []
    for k in lis:
        to_append = "('"+k+"')"
        if to_append not in insert_rows:
            insert_rows.append(to_append)
    if len(insert_rows) > 0:
        values = ', '.join(map(str, insert_rows))
        sql = "INSERT INTO workinglinks VALUES {}".format(values)
        # print(sql)
        cur = con.cursor() 
        cur.execute(sql)  
        con.commit()



def insert_package():
    a = datetime.now()
    con = connecting()
    con.row_factory = sqlite3.Row  
    cur = con.cursor()
    cur.execute("select * from workinglinks")
    rows = cur.fetchall() 
    lis = []
    for row in rows:
        lis.append(row[0])
    
    # print(lis)

    try:
        cur = con.cursor()
        cur.execute("select time from packageId")
        rows = cur.fetchall() 
        tim = rows[-1][0]
    except:
        tim = False
        pass


    if tim:
        t1 = datetime.strptime(tim,'%Y-%m-%d  %H:%M:%S.%f')
        # print(t1.day)
        # print(a.day)
        # exit()
        if t1.day == a.day:
            if  t1.hour+20 <= a.hour:
                con.execute('DELETE FROM packageId')
                con.commit()
        else:
            con.execute('DELETE FROM packageId')
            con.commit()
  
    str2 = ''
    # new_list = []
    for i in lis:
        str2 = str2 +'"'+ i+'"'+','
    cur = con.cursor() 
    query = '''SELECT PackageId FROM packageId WHERE PackageId in (''' +str2+''')'''
    query = query.replace(',)',')')
    cur.execute(query)  
    con.commit()
    rows = cur.fetchall() 
    insert_rows = []
    update_rows = []
    # print(rows)
    # print(lis)
    if len(rows) > 0 :
        for i in lis:
            # print(i[0])
            if i in [j[0] for j in rows]:
                # lis.remove(i)
                # new_list.append(i[0])
                update_rows.append("'"+str(i)+"'")

            else:
                to_append = "('"+i+"','"+str(a)+"','New_added','zzz')"
                if to_append not in insert_rows:
                    insert_rows.append(to_append)
    else:
        for i in lis:
            to_append = "('"+i+"','"+str(a)+"','New_added','zzz')"
            if to_append not in insert_rows:
                insert_rows.append(to_append)

    if len(insert_rows) > 0:
        values = ', '.join(map(str, insert_rows))
        sql = "INSERT INTO packageId VALUES {}".format(values)
        print(sql)
        cur = con.cursor() 
        cur.execute(sql)  
        con.commit()

    if len(update_rows) > 0 :
        values1 = ', '.join(map(str, update_rows))
        sql1 = "UPDATE packageId SET  app_status = 'old' WHERE PackageId in ({})".format(values1)

        cur = con.cursor()
        cur.execute(sql1)  
        con.commit()

    return True



