# from turtle import update
# from os import stat
import pandas as pd
import json
from datetime import datetime
import sqlite3
# import re as ser


# import playstore
# regex = '^[0-9][0-9][0-9][0-9][0-9]'









# check('12345')

# exit()
def updated():
    update_list = {}
    sheet_id='1yf3kHh37Y7hf8ciWVVkEOjfaTIBGifkuvTPa6a1-UUA'
    df=pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
    df_issue=pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?gid=60804224&format=csv") 

    dicts  = df.to_dict('records')
    issue_dicts  = df_issue.to_dict('records')
    new_list = []
    issue_list = []
    # print(dicts)
    for i in dicts:

        if i.get('live status') == 'Today/yesterday Converted':
            status = 'TRUE'
        else:
            status = 'FALSE'
        # print(i.get('New/Update'))
        tmp = {"Tracking":i.get('Tracking'),"Package_name":i.get('Application ID'),"New_update":i.get('New/Update'),"conversion":status, 'once':i.get('conversion status '), 'country':i.get('Country'),'last_update':i.get('Last Updated'),'Updated_by':i.get('Code Writer')}
        new_list.append(tmp)


    for i in issue_dicts:
        tmp = {"Package_name":i.get('Package_name'),"issue":i.get('Issue'),'Name':i.get('Name'),'Date':i.get('Date')}
        issue_list.append(tmp)

    return new_list,issue_list

    # print(update_list)
def get():
    updated_list,issue_list = updated()

    conn = sqlite3.connect('himanshu.db')
    conn.execute("create table IF NOT EXISTS updatedetails (Package_name TEXT  ,Tracking TEXT NOT NULL,NewORupdate TEXT,conversion TEXT,once TEXT,country TEXT,last_update TEXT, Updated_by TEXT )")  
    conn.execute("create table IF NOT EXISTS issueApp (Package_name TEXT  ,issue TEXT,Name TEXT,Date TEXT)")  
    # d = []
    with sqlite3.connect("himanshu.db") as con: 

        con.execute('DELETE FROM updatedetails')
        con.commit()
        for i in updated_list:
            if str(i.get('Package_name')) == 'nan' or '-' in str(i.get('Package_name')):
                # print(i.get('Package_name'))
                pass
            else:
                if len(i.get('Package_name')) <6 :
                    # if ser.search(regex, i.get('Package_name')) :
                    #     # print(i.get('Package_name'))
                    #     pass
                    # else:
                    #     pass
                    pass
                else:
                    # print("Invalid Name Enter Valid Name")
                    # d.append(i.get('Package_name'))
                    status = i.get('New_update')
                    # print(status)
                    cur = con.cursor() 
                    cur.execute("INSERT into updatedetails (Package_name ,Tracking,NewORupdate,conversion,once,country,last_update,Updated_by) values (?,?,?,?,?,?,?,?)",(i.get('Package_name').strip(),i.get('Tracking'),status,i.get('conversion'),i.get('once'),i.get('country'),i.get('last_update'),i.get('Updated_by')))  
                    con.commit()

    # print(d)
    with sqlite3.connect("himanshu.db") as con:  
        con.execute('DELETE FROM issueApp')
        con.commit()
        for i in issue_list:
            cur = con.cursor() 
            cur.execute("INSERT into issueApp (Package_name,issue,Name,Date) values (?,?,?,?)",(i.get('Package_name'),i.get('issue'),i.get('Name'),i.get('Date')))  
            con.commit()
    
    print("successful Done ........................")



# get()

# def show():
#     con = sqlite3.connect("himanshu.db")  
#     con.row_factory = sqlite3.Row  
#     cur = con.cursor()  
#     cur.execute("select * from updatedetails")
#     rows = cur.fetchall() 
#     for i in rows:
#         for j in i:
#             print(j,end=",")
#         print()
#     print("*"*200)
#     cur.execute("select * from issueApp")
#     rows = cur.fetchall() 
#     for i in rows:
#         for j in i:
#             print(j,end=",")
#         print()


# # show()




def refresh():

    updated_list,issue_list = updated()

    conn = sqlite3.connect('himanshu.db')
    conn.execute("create table IF NOT EXISTS updatedetails (Package_name TEXT  ,Tracking TEXT NOT NULL,NewORupdate TEXT,conversion TEXT,once TEXT,country TEXT,last_update TEXT, Updated_by TEXT )")  
    conn.execute("create table IF NOT EXISTS issueApp (Package_name TEXT  ,issue TEXT,Name TEXT,Date TEXT)")  
    # d = []
    with sqlite3.connect("himanshu.db") as con: 

        con.execute('DELETE FROM updatedetails')
        con.commit()
        for i in updated_list:
            if str(i.get('Package_name')) == 'nan' or '-' in str(i.get('Package_name')) or '/' in str(i.get('Package_name')) or ' ' in str(i.get('Package_name')):
                # print(i.get('Package_name'))
                pass
            else:
                if len(i.get('Package_name')) <6 :
                    # if ser.search(regex, i.get('Package_name')) :
                    #     # print(i.get('Package_name'))
                    #     pass
                    # else:
                    #     pass
                    pass
                else:
                    # print("Invalid Name Enter Valid Name")
                    # d.append(i.get('Package_name'))
                    # print(i.get('Tracking'))
                    # print(i.get('Package_name'))
                    cur = con.cursor() 
                    cur.execute("INSERT into updatedetails (Package_name ,Tracking,NewORupdate,conversion,once,country,last_update,Updated_by) values (?,?,?,?,?,?,?,?)",(i.get('Package_name').strip(),i.get('Tracking'),i.get('New_update'),i.get('conversion'),i.get('once'),i.get('country'),i.get('last_update'),i.get('Updated_by')))  
                    con.commit()

    # print(d)
    with sqlite3.connect("himanshu.db") as con:  
        con.execute('DELETE FROM issueApp')
        con.commit()
        for i in issue_list:
            cur = con.cursor() 
            cur.execute("INSERT into issueApp (Package_name,issue,Name,Date) values (?,?,?,?)",(i.get('Package_name'),i.get('issue'),i.get('Name'),i.get('Date')))  
            con.commit()
    
    print("successful Done ........................")




# refresh()















    # updated_list,issue_list = updated()

    # conn = sqlite3.connect('himanshu.db')
    # conn.execute("create table IF NOT EXISTS updatedetails (Package_name TEXT ,Tracking TEXT ,NewORupdate TEXT,conversion TEXT,once TEXT,country TEXT,last_update TEXT, Updated_by TEXT )")  
    
    # with sqlite3.connect("himanshu.db") as con:  
    #     for i in updated_list:
    #         cur = con.cursor() 
    #         cur.execute("INSERT into updatedetails (Package_name,Tracking,NewORupdate,conversion,once,country,last_update,Updated_by) values (?,?,?,?,?,?,?,?)",(i.get('Package_name'),i.get('Tracking'),i.get('New/update'),i.get('conversion'),i.get('once'),i.get('country'),i.get('last_update'),i.get('Updated_by')))  
    #         con.commit()
    
    # updated_dict = {}
    # issue_dict = {}
    # for i in updated_list:
    #     key = i.get('Package_name')
    #     if not key in updated_dict:
    #         updated_dict[key] = []
    #         updated_dict[key].append(i)
    #     else:
    #         if str(key) == "NaN" or str(key) == "nan":
    #             pass
    #         else:
    #             updated_dict[key].append(i)
    # for i in issue_list:
    #     key = i.get('Package_name')
    #     if not key in issue_dict:
    #         issue_dict[key] = []
    #         issue_dict[key].append(i)
    #     else:
    #         if str(key) == "NaN" or str(key) == "nan":
    #             pass
    #         else:
    #             issue_dict[key].append(i)

    # # print(updated)
    # print(updated_list)
    # conn = sqlite3.connect('himanshu.db')
    # conn.execute("create table IF NOT EXISTS updatedetails (PackageId TEXT ,time TEXT NOT NULL,app_status TEXT)")  
    # with open('update_details.py','w') as f:
    #     f.write('nan = False\n')
    #     f.write('NaN = False\n')
    #     f.write('updated_list = ')
    #     f.write(json.dumps(updated_dict))
    #     f.write('\n')
    #     f.write('\n')
    #     f.write('issue_dict = ')
    #     f.write(json.dumps(issue_dict))

  