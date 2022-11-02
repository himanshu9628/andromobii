

# from unicodedata import name
from dbconnect import get_db_connection as connecting
import sqlite3
from support import insert_package as fun2
from datetime import datetime
# import himanshudata
import requests,json


# himanshudata.refresh()



def working_link():
    con = connecting()
    con.row_factory = sqlite3.Row  
    cur = con.cursor()
    cur.execute("select * from workinglinks")
    rows = cur.fetchall() 
    lis = []
    for row in rows:
        lis.append(row[0])
    return lis



# import sqlite3
def get_data(*li):
    da = {}
    data = requests.get('https://appsdetails.herokuapp.com/appdata')
    tmp = json.loads(data.text)

    for i in li[0]:
        try:
            da[i] = tmp.get(i).get('category')
        except:
            da[i] = "Not Available"

    return da 








def get_appids():
    fun2()
    con = connecting()
    con.row_factory = sqlite3.Row  
    cur = con.cursor()
    cur.execute("select * from workinglinks")
    rows = cur.fetchall() 
    lis2 = []
    for row in rows:
        lis2.append(row[0])
    update_rows = []
    update_rows1 = []




    cur.execute("select packageId from packageId ORDER BY assign_to")
    rows = cur.fetchall() 
    lis = []
    for row in rows:
        lis.append(row[0])
    
    for x in lis:
        if x in lis2:
            update_rows.append("'"+str(x)+"'")
        else:
            update_rows1.append("'"+str(x)+"'")
        if len(update_rows) > 0 :
            values1 = ', '.join(map(str, update_rows))
            sql1 = "UPDATE packageId SET  app_status = 'Working' WHERE PackageId in ({})".format(values1)

            cur = con.cursor()
            cur.execute(sql1)  
            con.commit()
        if len(update_rows1) > 0 :
            values2 = ', '.join(map(str, update_rows1))
            sql2 = "UPDATE packageId SET  app_status = 'Not Working' WHERE PackageId in ({})".format(values2)

            cur = con.cursor()
            cur.execute(sql2)  
            con.commit()

    return lis


def get_individul(name):
    con = connecting()
    cur = con.cursor()
    que  ="SELECT * FROM 'teamdetails' WHERE Assign_to = '{}' ".format(name)
    cur.execute(que)
    row1 = cur.fetchall()
    # ('company.coinpop.coinpop', '2022-10-12 11:45:10.471631', 'New_added', 'No One')
    dic = {}
    r = []
    for i in range(len(row1)):
        if i < len(row1)-1 :
            if row1[i][0] == row1[i+1][0]:
                row1.remove(row1[i])
            else:
                pass
        else:
            pass
    for raw in row1:
        try:
            t = datetime.strptime(raw[1],'%Y-%m-%d  %H:%M:%S.%f')
            t1 = t.strftime('%d-%b')
        except:
            t1 = raw[1]
        try:
            t3 = datetime.strptime(raw[3],'%Y-%m-%d  %H:%M:%S.%f')
            t2 = t3.strftime('%d-%b')
        except:
            t2 = raw[3]
        # print(t1)
        # print(t2)
        dic[raw[0]] = {}
        dic[raw[0]]['Package_name'] = raw[0]
        dic[raw[0]]['assign_time'] = t1
        dic[raw[0]]['name'] = raw[2]
        dic[raw[0]]['done_time'] = t2
        dic[raw[0]]['status'] = raw[4]
    return dic

def get_individul_data():
    con = connecting()
    cur = con.cursor()
    que  ="SELECT * FROM 'teamdetails' WHERE checked = 'No' "
    cur.execute(que)
    row1 = cur.fetchall()
    # ('company.coinpop.coinpop', '2022-10-12 11:45:10.471631', 'New_added', 'No One')
    dic = {}
    r = []
    for x in row1:
        # print(i)
        try:
            t3 = datetime.strptime(x[1],'%Y-%m-%d  %H:%M:%S.%f')
            t2 = t3.strftime('%H:%M:%S')
        except:
            t2 = x[1]
        if not dic.get(x[2]):
            dic[x[2]] = []
            rmp = {"appid":x[0],'assign_time':t2}
            dic[x[2]].append(rmp)
        else:
            rmp = {"appid":x[0],'assign_time':t2}
            dic[x[2]].append(rmp)


    que1  ="SELECT * FROM 'teamdetails' WHERE checked = 'checked' "
    cur.execute(que1)
    row2 = cur.fetchall()
    # ('company.coinpop.coinpop', '2022-10-12 11:45:10.471631', 'New_added', 'No One')
    dic2 = {}
    r2 = []
    for z in row2:
        # print(i)

        if not dic2.get(z[2]):
            dic2[z[2]] = []
            rmp = {"appid":z[0],'done':z[3]}
            dic2[z[2]].append(rmp)
        else:
            rmp = {"appid":z[0],'done':z[3]}
            dic2[z[2]].append(rmp)
    
    return dic,dic2

def example():
    print("IN example")
    print("$"*100)

def deletedata():
    que1  ="SELECT * FROM 'teamdetails' WHERE checked = 'checked' "
    con = connecting()
    cur = con.cursor()
    cur.execute(que1)
    row2 = cur.fetchall()
    print(row2)
    r = []
    for x in row2:
        y = (x[0],x[2],x[3])
        r.append(y)
    values = ', '.join(map(str, r))
    print(values)
    print("*"*100)
    sql = "INSERT INTO donedetails VALUES {}".format(values)
    # print(r)
    cur = con.cursor() 
    cur.execute(sql)  
    con.commit()
    sql = "DELETE FROM 'teamdetails' WHERE checked = 'checked' "
    cur = con.cursor() 
    cur.execute(sql)  
    con.commit()
# deletedata()


def get_apps_data(*li):
    di = {}
    update = get_update_details()
    issue = get_issue_details()
    app_details = get_apps_details()
    for i in li[0]:
        di[i] = {}
        # print("&"*100)
        # print(i)
        # print("&"*100)
        try:
            di[i]['Tracking'] = update.get(i).get('Tracking')
        except:
            di[i]['Tracking'] = "Not Available"
        try:
            di[i]['NewORupdate'] = update.get(i).get('NewORupdate')
        except:
            di[i]['NewORupdate'] = "Not Available"
        try:
            di[i]['conversion'] = update.get(i).get('conversion')
        except:
            di[i]['conversion'] = "Not Available"
        try:
            di[i]['once'] = update.get(i).get('once')
        except:
            di[i]['once'] = "Not Available"
        try:
            di[i]['country'] = update.get(i).get('country')
        except:
            di[i]['country'] = "Not Available"
        try:
            di[i]['last_update'] = update.get(i).get('last_update')
        except:
            di[i]['last_update'] = "Not Available"
        try:
            di[i]['Updated_by'] = update.get(i).get('Updated_by')
        except:
            di[i]['Updated_by'] = "Not Available"
        try:
            di[i]['issue'] = issue.get(i).get('Issue')
        except:
            di[i]['issue'] = 'No issue'
        try:
            di[i]['assign_to'] = app_details.get(i).get('assign_to')
        except:
            di[i]['assign_to'] = "Not Available"
        try:
            di[i]['status'] = app_details.get(i).get('app_status')
        except:
            di[i]['status'] = "Not Availble"

    return di



def get_apps_details():
    con = connecting()
    cur = con.cursor()
    que  ="SELECT * FROM 'packageId' "
    cur.execute(que)
    row1 = cur.fetchall()
    # ('company.coinpop.coinpop', '2022-10-12 11:45:10.471631', 'New_added', 'No One')
    dic = {}
    # print(row1)
    for raw in row1:
        dic[raw[0]] = {}
        dic[raw[0]]['Package_name'] = raw[0]
        dic[raw[0]]['app_status'] = raw[2]
        dic[raw[0]]['assign_to'] = raw[3]
    return dic





def get_update_details():
    con = connecting()
    cur = con.cursor()
    que  ="SELECT * FROM 'updatedetails' "
    cur.execute(que)
    row1 = cur.fetchall()


    cur2 = con.cursor()
    que2  ="SELECT * FROM 'once' "
    cur2.execute(que2)
    row2 = cur2.fetchall()
    # # Package_name ,Tracking,NewORupdate,conversion,once,country,last_update,Updated_by
    # # ('com.dreame.reader', 'appsflyer', 'Update', 'FALSE', None, 'CA', '13-Sep', 'hitesh')

    temp = {}
    for r in row2:
        # print(r[0].strip())
        temp[r[0].strip()] = r[1]

    # print(temp)
    dic = {}
    for raw in row1:
        dic[raw[0]] = {}
        dic[raw[0]]['Package_name'] = raw[0]
        dic[raw[0]]['Tracking'] = raw[1]
        try:
            dic[raw[0]]['NewORupdate'] = raw[2]
        except:
            dic[raw[0]]['NewORupdate'] = None
        try:
            dic[raw[0]]['conversion'] = raw[3]
        except:
            dic[raw[0]]['conversion'] = None
        # print(temp.get(raw[0]))
        try:
            dic[raw[0]]['once'] = temp[raw[0]]
        except:
            dic[raw[0]]['once'] = temp.get(raw[0])
        try:
            dic[raw[0]]['country'] = raw[5]
        except:
            dic[raw[0]]['country'] = None
        try:
            dic[raw[0]]['last_update'] = raw[6]
        except:
            dic[raw[0]]['last_update'] = None
        try:
            dic[raw[0]]['Updated_by'] = raw[7]
        except:
            dic[raw[0]]['Updated_by'] = None
    # print(dic)
    return dic


# get_update_details()

def get_issue_details():
    con = connecting()
    cur = con.cursor()
    que = "SELECT * FROM 'issueeApp'"
    cur.execute(que)
    row1 = cur.fetchall()
    dic = {}
    for raw in row1:
        dic[raw[0]] = {}
        dic[raw[0]]['Package_name'] = raw[0]
        dic[raw[0]]['Issue'] = raw[1]

    return dic



# li = ['1300116604','ru.more.play','com.brandicorp.brandi3']
# print(get_apps_data(li))
