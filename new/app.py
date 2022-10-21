


import sqlite3
import appDetails
from flask import Flask, jsonify,render_template,request,redirect,url_for
# from flask_restful import Resource, Api
from datetime import datetime
import himanshudata
import json,requests
# creating the flask app
app = Flask(__name__)
# creating an API object
# api = Api(app)
# from model import fatch_home_data

# exit()
# t = []

# @app.route('/', methods=['GET','POST'])
# def my_form_post2():
#     if request.method == 'GET':
#         return render_template('inputData.html')
#     else:
#         li = request.form['text2']
#         t = li.split(' ')
#     return "true"

def get_db_connection():
    conn = sqlite3.connect('himanshu.db')
    # conn.row_factory = sqlite3.Row
    conn.execute("create table IF NOT EXISTS packageId (PackageId TEXT PRIMARY KEY,time TEXT NOT NULL,app_status TEXT DEFAULT 'Not')")  
  
# print("Table created successfully")  
    return conn


# @app.route('/hell')
# def fatch_home_data2():
#     return "hello"



@app.route('/Home')
def my_form_post():
    get_id()
    return redirect(url_for('Home2'))

        
@app.route('/')
def Home():
    # from test import fatch_home_data1
    # fatch_home_data1()

    return "hello"
    # return  render_template('outputData.html')


        
@app.route('/Home2')
def Home2():
    
    new_list1 = {'output':[],'test':{},"cat":"HOME","status":{}}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    # package_list = 
    cur = con.cursor()  
    quer = que  ="SELECT *  FROM 'packageId1' ORDER BY app_status"
    cur.execute(quer)
    rows1 = cur.fetchall()
    list2 = [dict(ix) for ix in rows1]

    for j in list2:
        i = j.get('PackageId')
        cur = con.cursor()  
        quer = que  ="SELECT app_status FROM 'packageId1' WHERE PackageId = '"+i+"'"
        cur.execute(quer)
        rows1 = cur.fetchall()
        package_list = [dict(ix) for ix in rows1]

        new_list1['status'][i] = []
        new_list1['status'][i].append(package_list[0].get('app_status'))
        new_list1['output'].append(i)
        new_list1['test'][i] = []
        cur = con.cursor()
        que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
        que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
        cur.execute(que)
        row1 = cur.fetchall()
        updated_list = [dict(ix) for ix in row1]
        # print(updated_list)
        # exit()
        cur = con.cursor()
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
        # except:
        #     new_list1['test'][i].append("Not")
        #     new_list1['test'][i].append("Not")
        #     # pass
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
        # print(new_list1)
        # print(new_list1)
        # exit()
    return  render_template('newdata.html',out_data=new_list1)






    # return render_template('outputData.html',out_data=out)


@app.route('/d')
def refresh():
    refres = {'test':'1'}
    # print("hrello")
    himanshudata.refresh()
    return redirect('/')


@app.route('/details')
def details():
    args = request.args
    out = {"package":args.get('id')}
    que1  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+args.get('id')+"'"
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute(que1)
    row1 = cur.fetchall()
    updated_list = [dict(ix) for ix in row1]
    if updated_list:
        out['id'] = updated_list
    else:
        out['id'] = [{}]

    return render_template('details.html',out_data=out)


@app.route('/issue')
def issue():
    args = request.args
    out = {"package":args.get('id')}
    que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+args.get('id')+"'"
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute(que1)
    row1 = cur.fetchall()
    issue_dict = [dict(ix) for ix in row1]
    if issue_dict:
        out['id'] = issue_dict
    else:
        out['id'] = [{}]

    return render_template('issue.html',out_data=out)




@app.route('/Utilities')
def Utilities():
    # print("IN ljkjk"*100)
    Utilities = {'output':[],'test':{},"cat":"Utilities"}
    # Utilities = {'test':[]}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:
        # print appDetails.App_data.get(i).get('category')  
            if appDetails.App_data.get(i).get('category') == "Utilities":
                # print(i)
                Utilities['output'].append(i)
                Utilities['test'][i] = []
                cur = con.cursor()
                que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
                que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
                cur.execute(que)
                row1 = cur.fetchall()
                updated_list = [dict(ix) for ix in row1]

                cur = con.cursor()
                cur.execute(que1)
                row2 = cur.fetchall()
                issue_dict = [dict(ix) for ix in row2]
                # print(issue_list)
                # print("*"*122)
                if updated_list:
                    Utilities['country'] = updated_list[-1].get('country')
                else:
                    Utilities['country'] = 'us'
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False     
                    Utilities['test'][i].append(updated_list[-1].get('last_update'))
                    Utilities['test'][i].append(updated_list[-1].get('conversion'))
                    Utilities['test'][i].append(once)
                    Utilities['test'][i].append(updated_list[-1].get('Updated_by'))
                else:
                    try:
                        Utilities['test'][i].append(issue_dict[-1].get('Date'))
                        Utilities['test'][i].append("Issue")
                        Utilities['test'][i].append("False")
                        Utilities['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        Utilities['test'][i].append("Not Available")
                        Utilities['test'][i].append("Not Available")
                        Utilities['test'][i].append("Not Available")
                        Utilities['test'][i].append("Not Available")

                
        except:
            pass    
        # print(Utilities)
    return  render_template('outputData.html',out_data=Utilities)






@app.route('/games')
def games():
    Games = {'output':[],'test':{},"cat":"Games"}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:
            if  appDetails.App_data.get(i).get('category') == "Games":
                # print i
                Games['output'].append(i)
                Games['test'][i] = []
                cur = con.cursor()
                que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
                que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
                cur.execute(que)
                row1 = cur.fetchall()
                updated_list = [dict(ix) for ix in row1]

                cur = con.cursor()
                cur.execute(que1)
                row2 = cur.fetchall()
                issue_dict = [dict(ix) for ix in row2]
                if updated_list:
                    Games['country'] = updated_list[-1].get('country')
                else:
                    Games['country'] = 'us'
                
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False
                    Games['test'][i].append(updated_list[-1].get('last_update'))
                    Games['test'][i].append(updated_list[-1].get('conversion'))
                    Games['test'][i].append(once)
                    Games['test'][i].append(updated_list[-1].get('Updated_by'))

                else:
                    try:
                        Games['test'][i].append(issue_dict[-1].get('Date'))
                        Games['test'][i].append("Issue")
                        Games['test'][i].append("False")
                        Games['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        Games['test'][i].append("Not Available")
                        Games['test'][i].append("Not Available")
                        Games['test'][i].append("Not Available")
                        Games['test'][i].append("Not Available")

        except:
            pass  
    return  render_template('outputData.html',out_data=Games)

@app.route('/Tools')
def Tools():
    Tools = {'output':[],'test':{},"cat":"Tools"}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:

        # print appDetails.App_data.get(i).get('category')  
            if  appDetails.App_data.get(i).get('category') == "Tools":
                # print i
                Tools['output'].append(i)
                Tools['test'][i] = []
                cur = con.cursor()
                que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
                que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
                cur.execute(que)
                row1 = cur.fetchall()
                updated_list = [dict(ix) for ix in row1]

                cur = con.cursor()
                cur.execute(que1)
                row2 = cur.fetchall()
                issue_dict = [dict(ix) for ix in row2]
                if updated_list:
                    Tools['country'] = updated_list[-1].get('country')
                else:
                    Tools['country'] = 'us'
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False
                    Tools['test'][i].append(updated_list[-1].get('last_update'))
                    Tools['test'][i].append(updated_list[-1].get('conversion'))
                    Tools['test'][i].append(once)
                    Tools['test'][i].append(updated_list[-1].get('Updated_by'))

                else:
                    try:
                        Tools['test'][i].append(issue_dict[-1].get('Date'))
                        Tools['test'][i].append("Issue")
                        Tools['test'][i].append("False")
                        Tools['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        Tools['test'][i].append("Not Available")
                        Tools['test'][i].append("Not Available")
                        Tools['test'][i].append("Not Available")
                        Tools['test'][i].append("Not Available")
        except:
            pass    
    return  render_template('outputData.html',out_data=Tools)

@app.route('/travel')
def Travel():
    Travel = {'output':[],'test':{},"cat":"Vehicles and Travels"}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:

        # print appDetails.App_data.get(i).get('category')  
            if  appDetails.App_data.get(i).get('category') == "Vehicles and Travels":
                # print i
                Travel['output'].append(i)
                Travel['test'][i] = []
                cur = con.cursor()
                que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
                que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
                cur.execute(que)
                row1 = cur.fetchall()
                updated_list = [dict(ix) for ix in row1]

                cur = con.cursor()
                cur.execute(que1)
                row2 = cur.fetchall()
                issue_dict = [dict(ix) for ix in row2]
                if updated_list:
                    Travel['country'] = updated_list[-1].get('country')
                else:
                    Travel['country'] = 'us'
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False
                    Travel['test'][i].append(updated_list[-1].get('last_update'))
                    Travel['test'][i].append(updated_list[-1].get('conversion'))
                    Travel['test'][i].append(once)
                    Travel['test'][i].append(updated_list[-1].get('Updated_by'))

                else:
                    try:
                        Travel['test'][i].append(issue_dict[-1].get('Date'))
                        Travel['test'][i].append("Issue")
                        Travel['test'][i].append("False")
                        Travel['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        Travel['test'][i].append("Not Available")
                        Travel['test'][i].append("Not Available")
                        Travel['test'][i].append("Not Available")
                        Travel['test'][i].append("Not Available")
        except:
            pass    
    return  render_template('outputData.html',out_data=Travel)

@app.route('/Entertainment')
def Entertainment():
    Entertainment = {'output':[],'test':{},"cat":"Entertainment"}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:

        # print appDetails.App_data.get(i).get('category')  
            if  appDetails.App_data.get(i).get('category') == "Entertainment":
                # print i
                Entertainment['output'].append(i)
                Entertainment['test'][i] = []
                cur = con.cursor()
                que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
                que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
                cur.execute(que)
                row1 = cur.fetchall()
                updated_list = [dict(ix) for ix in row1]

                cur = con.cursor()
                cur.execute(que1)
                row2 = cur.fetchall()
                issue_dict = [dict(ix) for ix in row2]
                if updated_list:
                    Entertainment['country'] = updated_list[-1].get('country')
                else:
                    Entertainment['country'] = 'us'

                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False
                    # try:
                        # Entertainment['test'][i].append(appDetails.App_data.get(i).get('updated'))
                    Entertainment['test'][i].append(updated_list[-1].get('last_update'))
                    Entertainment['test'][i].append(updated_list[-1].get('conversion'))
                    Entertainment['test'][i].append(once)
                    Entertainment['test'][i].append(updated_list[-1].get('Updated_by'))

                else:
                    try:
                        Entertainment['test'][i].append(issue_dict[-1].get('Date'))
                        Entertainment['test'][i].append("Issue")
                        Entertainment['test'][i].append("False")
                        Entertainment['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        Entertainment['test'][i].append("Not Available")
                        Entertainment['test'][i].append("Not Available")
                        Entertainment['test'][i].append("Not Available")
                        Entertainment['test'][i].append("Not Available")
        except:
            pass    
    return  render_template('outputData.html',out_data=Entertainment)

@app.route('/Education')
def Education():
    Education = {'output':[],'test':{},"cat":"Books and Education"}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:

        # print appDetails.App_data.get(i).get('category')  
            if  appDetails.App_data.get(i).get('category') == "Education and Books":
                # print i
                Education['output'].append(i)
                Education['test'][i] = []
                cur = con.cursor()
                que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
                que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
                cur.execute(que)
                row1 = cur.fetchall()
                updated_list = [dict(ix) for ix in row1]

                cur = con.cursor()
                cur.execute(que1)
                row2 = cur.fetchall()
                issue_dict = [dict(ix) for ix in row2]
                if updated_list:
                    Education['country'] = updated_list[-1].get('country')
                else:
                    Education['country'] = 'us'
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False
                    # try:
                        # Education['test'][i].append(appDetails.App_data.get(i).get('updated'))
                    Education['test'][i].append(updated_list[-1].get('last_update'))
                    Education['test'][i].append(updated_list[-1].get('conversion'))
                    Education['test'][i].append(once)
                    Education['test'][i].append(updated_list[-1].get('Updated_by'))

                else:
                    try:
                        Education['test'][i].append(issue_dict[-1].get('Date'))
                        Education['test'][i].append("Issue")
                        Education['test'][i].append("False")
                        Education['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        Education['test'][i].append("Not Available")
                        Education['test'][i].append("Not Available")
                        Education['test'][i].append("Not Available")
                        Education['test'][i].append("Not Available")
        except:
            pass    
    return  render_template('outputData.html',out_data=Education)

@app.route('/Food')
def Food():
    Food = {'output':[],'test':{},"cat":"Food and Drinks"}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:

        # print appDetails.App_data.get(i).get('category')  
            if  appDetails.App_data.get(i).get('category') == "Food & Drink":
                # print i
                Food['output'].append(i)
                Food['test'][i] = []
                cur = con.cursor()
                que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
                que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
                cur.execute(que)
                row1 = cur.fetchall()
                updated_list = [dict(ix) for ix in row1]

                cur = con.cursor()
                cur.execute(que1)
                row2 = cur.fetchall()
                issue_dict = [dict(ix) for ix in row2]
                if updated_list:
                    Food['country'] = updated_list[-1].get('country')
                else:
                    Food['country'] = 'us'
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False
                    # try:
                        # Food['test'][i].append(appDetails.App_data.get(i).get('updated'))
                    Food['test'][i].append(updated_list[-1].get('last_update'))
                    Food['test'][i].append(updated_list[-1].get('conversion'))
                    Food['test'][i].append(once)
                    Food['test'][i].append(updated_list[-1].get('Updated_by'))

                else:
                    try:
                        Food['test'][i].append(issue_dict[-1].get('Date'))
                        Food['test'][i].append("Issue")
                        Food['test'][i].append("False")
                        Food['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        Food['test'][i].append("Not Available")
                        Food['test'][i].append("Not Available")
                        Food['test'][i].append("Not Available")
                        Food['test'][i].append("Not Available")
        except:
            pass    
    return  render_template('outputData.html',out_data=Food)

@app.route('/Social')
def Social():
    Social = {'output':[],'test':{},"cat":"Social and Communication"}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:

        # print appDetails.App_data.get(i).get('category')  
            if  appDetails.App_data.get(i).get('category') == "Social and Communication":
                # print i
                Social['output'].append(i)
                Social['test'][i] = []
                cur = con.cursor()
                que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
                que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
                cur.execute(que)
                row1 = cur.fetchall()
                updated_list = [dict(ix) for ix in row1]

                cur = con.cursor()
                cur.execute(que1)
                row2 = cur.fetchall()
                issue_dict = [dict(ix) for ix in row2]
                if updated_list:
                    Social['country'] = updated_list[-1].get('country')
                else:
                    Social['country'] = 'us'
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False
                    # try:
                        # Social['test'][i].append(appDetails.App_data.get(i).get('updated'))
                    Social['test'][i].append(updated_list[-1].get('last_update'))
                    Social['test'][i].append(updated_list[-1].get('conversion'))
                    Social['test'][i].append(once)
                    Social['test'][i].append(updated_list[-1].get('Updated_by'))

                else:
                    try:
                        Social['test'][i].append(issue_dict[-1].get('Date'))
                        Social['test'][i].append("Issue")
                        Social['test'][i].append("False")
                        Social['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        Social['test'][i].append("Not Available")
                        Social['test'][i].append("Not Available")
                        Social['test'][i].append("Not Available")
                        Social['test'][i].append("Not Available")
        except:
            pass    
    return  render_template('outputData.html',out_data=Social)

@app.route('/Casino')
def Casino():
    Casino = {'output':[],'test':{},"cat":"Casino"}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:

        # print appDetails.App_data.get(i).get('category')  
            if  appDetails.App_data.get(i).get('category') == "Casino":
                # print i
                Casino['output'].append(i)
                Casino['test'][i] = []
                cur = con.cursor()
                que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
                que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
                cur.execute(que)
                row1 = cur.fetchall()
                updated_list = [dict(ix) for ix in row1]

                cur = con.cursor()
                cur.execute(que1)
                row2 = cur.fetchall()
                issue_dict = [dict(ix) for ix in row2]
                if updated_list:
                    Casino['country'] = updated_list[-1].get('country')
                else:
                    Casino['country'] = 'us'
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False
                    # try:
                        # Casino['test'][i].append(appDetails.App_data.get(i).get('updated'))
                    Casino['test'][i].append(updated_list[-1].get('last_update'))
                    Casino['test'][i].append(updated_list[-1].get('conversion'))
                    Casino['test'][i].append(once)
                    Casino['test'][i].append(updated_list[-1].get('Updated_by'))

                else:
                    try:
                        Casino['test'][i].append(issue_dict[-1].get('Date'))
                        Casino['test'][i].append("Issue")
                        Casino['test'][i].append("False")
                        Casino['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        Casino['test'][i].append("Not Available")
                        Casino['test'][i].append("Not Available")
                        Casino['test'][i].append("Not Available")
                        Casino['test'][i].append("Not Available")
        except:
            pass    
    return  render_template('outputData.html',out_data=Casino)

@app.route('/House')
def House():
    House = {'output':[],'test':{},"cat":"House and Home"}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:

        # print appDetails.App_data.get(i).get('category')  
            if  appDetails.App_data.get(i).get('category') == "House & Home":
                # print i
                House['output'].append(i)
                House['test'][i] = []
                cur = con.cursor()
                que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
                que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
                cur.execute(que)
                row1 = cur.fetchall()
                updated_list = [dict(ix) for ix in row1]

                cur = con.cursor()
                cur.execute(que1)
                row2 = cur.fetchall()
                issue_dict = [dict(ix) for ix in row2]
                if updated_list:
                    House['country'] = updated_list[-1].get('country')
                else:
                    House['country'] = 'us'
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False

                    House['test'][i].append(updated_list[-1].get('last_update'))
                    House['test'][i].append(updated_list[-1].get('conversion'))
                    House['test'][i].append(once)
                    House['test'][i].append(updated_list[-1].get('Updated_by'))

                else:
                    try:
                        House['test'][i].append(issue_dict[-1].get('Date'))
                        House['test'][i].append("Issue")
                        House['test'][i].append("False")
                        House['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        House['test'][i].append("Not Available")
                        House['test'][i].append("Not Available")
                        House['test'][i].append("Not Available")
                        House['test'][i].append("Not Available")
        except:
            pass    
    return  render_template('outputData.html',out_data=House)

@app.route('/Lifestyle')
def Lifestyle():
    Lifestyle = {'output':[],'test':{},"cat":"Lifestyle"}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:

        # print appDetails.App_data.get(i).get('category')  
            if  appDetails.App_data.get(i).get('category') == "Lifestyle":
                # print i
                Lifestyle['output'].append(i)
                Lifestyle['test'][i] = []
                cur = con.cursor()
                que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
                que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
                cur.execute(que)
                row1 = cur.fetchall()
                updated_list = [dict(ix) for ix in row1]

                cur = con.cursor()
                cur.execute(que1)
                row2 = cur.fetchall()
                issue_dict = [dict(ix) for ix in row2]
                if updated_list:
                    Lifestyle['country'] = updated_list[-1].get('country')
                else:
                    Lifestyle['country'] = 'us'
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False
                    # try:
                        # Lifestyle['test'][i].append(appDetails.App_data.get(i).get('updated'))
                    Lifestyle['test'][i].append(updated_list[-1].get('last_update'))
                    Lifestyle['test'][i].append(updated_list[-1].get('conversion'))
                    Lifestyle['test'][i].append(once)
                    Lifestyle['test'][i].append(updated_list[-1].get('Updated_by'))

                else:
                    try:
                        Lifestyle['test'][i].append(issue_dict[-1].get('Date'))
                        Lifestyle['test'][i].append("Issue")
                        Lifestyle['test'][i].append("False")
                        Lifestyle['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        Lifestyle['test'][i].append("Not Available")
                        Lifestyle['test'][i].append("Not Available")
                        Lifestyle['test'][i].append("Not Available")
                        Lifestyle['test'][i].append("Not Available")
        except:
            pass    
    return  render_template('outputData.html',out_data=Lifestyle)

@app.route('/Health')
def Health():
    Health = {'output':[],'test':{},"cat":"Health and Fitness"}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:

        # print appDetails.App_data.get(i).get('category')  
            if  appDetails.App_data.get(i).get('category') == "Health and Fitness":
                # print i
                Health['output'].append(i)
                Health['test'][i] = []
                cur = con.cursor()
                que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
                que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
                cur.execute(que)
                row1 = cur.fetchall()
                updated_list = [dict(ix) for ix in row1]

                cur = con.cursor()
                cur.execute(que1)
                row2 = cur.fetchall()
                issue_dict = [dict(ix) for ix in row2]
                if updated_list:
                    Health['country'] = updated_list[-1].get('country')
                else:
                    Health['country'] = 'us'
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False
                    # try:
                        # Health['test'][i].append(appDetails.App_data.get(i).get('updated'))
                    Health['test'][i].append(updated_list[-1].get('last_update'))
                    Health['test'][i].append(updated_list[-1].get('conversion'))
                    Health['test'][i].append(once)
                    Health['test'][i].append(updated_list[-1].get('Updated_by'))

                else:
                    try:
                        Health['test'][i].append(issue_dict[-1].get('Date'))
                        Health['test'][i].append("Issue")
                        Health['test'][i].append("False")
                        Health['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        Health['test'][i].append("Not Available")
                        Health['test'][i].append("Not Available")
                        Health['test'][i].append("Not Available")
                        Health['test'][i].append("Not Available")
        except:
            pass    
    return  render_template('outputData.html',out_data=Health)

@app.route('/Shopping')
def Shopping():
    Shopping = {'output':[],'test':{},"cat":"Shopping"}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:

        # print appDetails.App_data.get(i).get('category')  
            if  appDetails.App_data.get(i).get('category') == "Shopping":
                # print i
                Shopping['output'].append(i)
                Shopping['test'][i] = []
                cur = con.cursor()
                que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
                que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
                cur.execute(que)
                row1 = cur.fetchall()
                updated_list = [dict(ix) for ix in row1]

                cur = con.cursor()
                cur.execute(que1)
                row2 = cur.fetchall()
                issue_dict = [dict(ix) for ix in row2]
                if updated_list:
                    Shopping['country'] = updated_list[-1].get('country')
                else:
                    Shopping['country'] = 'us'
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False
                    # try:
                        # Shopping['test'][i].append(appDetails.App_data.get(i).get('updated'))
                    Shopping['test'][i].append(updated_list[-1].get('last_update'))
                    Shopping['test'][i].append(updated_list[-1].get('conversion'))
                    Shopping['test'][i].append(once)
                    Shopping['test'][i].append(updated_list[-1].get('Updated_by'))

                else:
                    try:
                        Shopping['test'][i].append(issue_dict[-1].get('Date'))
                        Shopping['test'][i].append("Issue")
                        Shopping['test'][i].append("False")
                        Shopping['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        Shopping['test'][i].append("Not Available")
                        Shopping['test'][i].append("Not Available")
                        Shopping['test'][i].append("Not Available")
                        Shopping['test'][i].append("Not Available")
        except:
            pass    
    return  render_template('outputData.html',out_data=Shopping)

@app.route('/Finance')
def Finance():
    Finance = {'output':[],'test':{},"cat":"Finance"}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:

        # print appDetails.App_data.get(i).get('category')  
            if  appDetails.App_data.get(i).get('category') == "Finance":
                # print i
                Finance['output'].append(i)
                Finance['test'][i] = []
                cur = con.cursor()
                que  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+i+"'"
                que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+i+"'"
                cur.execute(que)
                row1 = cur.fetchall()
                updated_list = [dict(ix) for ix in row1]

                cur = con.cursor()
                cur.execute(que1)
                row2 = cur.fetchall()
                issue_dict = [dict(ix) for ix in row2]
                if updated_list:
                    Finance['country'] = updated_list[-1].get('country')
                else:
                    Finance['country'] = 'us'
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False
                    # try:
                        # Finance['test'][i].append(appDetails.App_data.get(i).get('updated'))
                    Finance['test'][i].append(updated_list[-1].get('last_update'))
                    Finance['test'][i].append(updated_list[-1].get('conversion'))
                    Finance['test'][i].append(once)
                    Finance['test'][i].append(updated_list[-1].get('Updated_by'))

                else:
                    try:
                        Finance['test'][i].append(issue_dict[-1].get('Date'))
                        Finance['test'][i].append("Issue")
                        Finance['test'][i].append("False")
                        Finance['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        Finance['test'][i].append("Not Available")
                        Finance['test'][i].append("Not Available")
                        Finance['test'][i].append("Not Available")
                        Finance['test'][i].append("Not Available")
        except:
            pass    
    return  render_template('outputData.html',out_data=Finance)

@app.route('/Not1')
def Not1():
    Not1 = {'output':[],'test':{},"cat":"Categories not Available"}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:

        # print appDetails.App_data.get(i).get('category')  
            if  appDetails.App_data.get(i).get('category') == "Not available":
                # print i
                Not1['output'].append(i)
                Not1['test'][i] = []
                if updated_list:
                    Not1['country'] = updated_list[-1].get('country')
                else:
                    Not1['country'] = 'us'
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False
                    # try:
                        # Not1['test'][i].append(appDetails.App_data.get(i).get('updated'))
                    Not1['test'][i].append(updated_list[-1].get('last_update'))
                    Not1['test'][i].append(updated_list[-1].get('conversion'))
                    Not1['test'][i].append(once)
                    Not1['test'][i].append(updated_list[-1].get('Updated_by'))

                else:
                    try:
                        Not1['test'][i].append(issue_dict[-1].get('Date'))
                        Not1['test'][i].append("Issue")
                        Not1['test'][i].append("False")
                        Not1['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        Not1['test'][i].append("Not Available")
                        Not1['test'][i].append("Not Available")
                        Not1['test'][i].append("Not Available")
                        Not1['test'][i].append("Not Available")
        except:
            pass    
    return  render_template('outputData.html',out_data=Not1)
@app.route('/Notavailable')
def Not2():
    Not2 = {'output':[],'test':{},"cat":"No Data Found"}
    con = sqlite3.connect("himanshu.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute("select PackageId from packageId1")
    rows = cur.fetchall() 
    # for row in rows:
    # print(rows)
    # with open('t.txt') as f:
    #     s = f.read()
    for j in rows:
        i = j[0]
        # print(i)
        try:

        # print appDetails.App_data.get(i).get('category')  
            if not appDetails.App_data.get(i):
                # print i
                if updated_list:
                    Not2['country'] = updated_list[-1].get('country')
                else:
                    Not2['country'] = 'us'




                Not2['output'].append(i)
                scraper.app_list(i)
                Not2['test'][i] = []
                if updated_list:
                    for j in updated_list:
                        if j.get('once') == "TRUE":
                            once = "TRUE"
                            break
                        else:
                            once = False
                    # Not2['test'][i].append("Not")
                    Not2['test'][i].append(updated_list[-1].get('last_update'))
                    Not2['test'][i].append(updated_list[-1].get('conversion'))
                    Not2['test'][i].append(once)
                    Not2['test'][i].append(updated_list[-1].get('Updated_by'))
                else:
                    try:
                        Not2['test'][i].append(issue_dict[-1].get('Date'))
                        Not2['test'][i].append("Issue")
                        Not2['test'][i].append("False")
                        Not2['test'][i].append(issue_dict[-1].get('Name'))
                    except:
                        Not2['test'][i].append("Not Available")
                        Not2['test'][i].append("Not Available")
                        Not2['test'][i].append("Not Available")
                        Not2['test'][i].append("Not Available")
        except:
            pass    
    # scraper.app_list(Not2.get('output'))
    return  render_template('outputData.html',out_data=Not2)

# # @app.route('/utilities')
# # def utility():
# #     return  render_template('games.html',out_data=Utilities)

# # @app.route('/tools')
# # def tools():
# #     return  render_template('outputData.html',out_data=Tools)

from controler import get_id,getdata
import test

@app.route('/_get_ajax_data/')
def get_ajax_data():
    data = {"hello": "world"}
    response = jsonify(data)
    response.cache_control.max_age = 60 * 60 * 24  # 1 day (in seconds)
    return response  


if __name__ == '__main__':
    app.run(debug = True)

