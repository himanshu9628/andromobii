
from datetime import datetime
from app import app,get_db_connection
import requests,json,sqlite3
import himanshudata


def get_id():
    # refres = {'test':'0'}
    print("in get id ")
    # refres = {'list': []}
    a = datetime.now()


    url = "https://affise.c2a.in/app_working_link.php?fetch_campaigns=List+Campaigns"

    res = requests.get(url)
    t = json.loads(res.text)
    lis = t.get('suggestedApps')
    # refres['list'] = lis
    print(lis)
    get_db_connection()
    con = sqlite3.connect("himanshu.db")  
    # con.row_factory = sqlite3.Row  

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
        if t1.day != a.day:
            con.execute('DELETE FROM packageId')
            con.commit()
        else:
            pass
    cur = con.cursor() 
    query = "SELECT PackageId FROM packageId WHERE app_status = 'checked'"
    print("Q"*100)
    print(query)
    cur.execute(query)  
    con.commit()
    # print(t)
    rows = cur.fetchall() 
    # print(rows)
    newlis = []
    insert_rows = []
    # update_rows = []
    if len(rows) > 0 :
        for j in rows:
            newlis.append(j[0])
    # print("new"*100)
    # print(newlis)
    str2 = ''
    for i in newlis:
        str2 = str2 +'"'+ i+'"'+','
        if i in lis:
            lis.remove(i)
    cur = con.cursor() 
    query = '''DELETE  FROM packageId WHERE PackageId not in (''' +str2+''')'''
    query = query.replace(',)',')')
    print(query)
    con.execute(query)
    con.commit()

    for k in lis:
        to_append = "('"+k+"','"+str(a)+"','Not')"
        if to_append not in insert_rows:
            insert_rows.append(to_append)
    if len(insert_rows) > 0:
        values = ', '.join(map(str, insert_rows))
        sql = "INSERT INTO packageId VALUES {}".format(values)
        # print(sql)
        cur = con.cursor() 
        cur.execute(sql)  
        con.commit()
# get_id()