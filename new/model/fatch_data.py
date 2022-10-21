


# from app import get_db_connection
import sqlite3,json
import appDetails



def get_db_connection():
    conn = sqlite3.connect('himanshu.db')
    # conn.row_factory = sqlite3.Row
    conn.execute("create table IF NOT EXISTS packageId (PackageId TEXT PRIMARY KEY,time TEXT NOT NULL,app_status TEXT DEFAULT 'Not')")  
  


class get_data():

    def __init__(self):
        get_db_connection()
        self.con = sqlite3.connect("himanshu.db") 
        self.cur = self.con.cursor()
    def get_home_data(self):
        new_list1 = {'output':[],'test':{},"cat":"HOME","status":{}}
        with sqlite3.connect("himanshu.db") as con:  
            con.row_factory = sqlite3.Row
            quer ="SELECT *  FROM 'packageId' ORDER BY app_status"
            cur = con.cursor()
            cur.execute(quer)
            rows1 = cur.fetchall()
            print("roe"*100)
            print(rows1)
            list2 = [dict(ix) for ix in rows1]
            for j in list2:
                i = j.get('PackageId')
                # cur = self.con.cursor()  
                quer   ="SELECT app_status FROM 'packageId' WHERE PackageId = '"+i+"'"
                cur.execute(quer)
                rows1 = cur.fetchall()
                package_list = [dict(ix) for ix in rows1]
                
                new_list1['status'][i] = []
                new_list1['status'][i].append(package_list[0].get('app_status'))
                new_list1['output'].append(i)
                new_list1['test'][i] = []
                # cur = self.con.cursor()
                que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
                que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
                cur.execute(que)
                row1 = cur.fetchall()
                updated_list = [dict(ix) for ix in row1]
                # print(updated_list)
                # exit()
                # cur = con.cursor()
                cur.execute(que1)
                row2 = cur.fetchall()
                issue_dict = [dict(ix) for ix in row2]
                # try:
                # print("*"*100)
                # print(i)
                # print("*"*100)
                if appDetails.App_data.get(i):
                    new_list1['test'][i].append(appDetails.App_data.get(i).get('category'))
                else:
                    # new_list1['test'][i].append("Not")
                    new_list1['test'][i].append("Not")

                if updated_list:
                    new_list1['country'] = updated_list[-1].get('country')
                else:
                    new_list1['country'] = 'us'
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False
                    new_list1['test'][i].append(updated_list[-1].get('last_update'))
                    new_list1['test'][i].append(updated_list[-1].get('conversion'))
                    new_list1['test'][i].append(once)
                    new_list1['test'][i].append(updated_list[-1].get('Tracking'))
                    new_list1['test'][i].append(updated_list[-1].get('NewORupdate'))
                    new_list1['test'][i].append(updated_list[-1].get('Updated_by'))

                else:
                    try:
                        new_list1['test'][i].append(issue_dict[-1].get('Date'))
                        new_list1['test'][i].append("Issue")
                        new_list1['test'][i].append("Not Available")
                        new_list1['test'][i].append("Not Available")
                        new_list1['test'][i].append("Not Available")
                        new_list1['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        new_list1['test'][i].append("Not Available")
                        new_list1['test'][i].append("Not Available")
                        new_list1['test'][i].append("Not Available")
                        new_list1['test'][i].append("Not Available")
                        new_list1['test'][i].append("Not Available")
                        new_list1['test'][i].append("Not Available")

        return json.dumps(new_list1)
