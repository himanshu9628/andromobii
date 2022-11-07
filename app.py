


import sqlite3

# from turtle import update
import appDetails
# import imp
from flask import Flask, jsonify,render_template,request,redirect,url_for,session,send_file
# from flask_restful import Resource, Api
from datetime import datetime
import himanshudata
import json,requests,random
from flask_apscheduler import APScheduler
from support import refresh as fun
from support import insert_package as fun2
from fatchData import example as fun3
from fatchData import get_appids
from fatchData import deletedata
from fatchData import get_apps_data,get_individul,get_data,get_issue_details,working_link,get_individul_data
from dbconnect import get_db_connection as get_db_connection
app = Flask(__name__)


scheduler = APScheduler()
scheduler.init_app(app)

app.apscheduler.add_job(func=fun, trigger='interval', seconds=300,id=str(random.randint(1,3)))
# app.apscheduler.add_job(func=fun3, trigger='interval', seconds=300,id=str(random.randint(1,3)))

scheduler.start()



@app.route('/form')
def form():
    return render_template('newform.html')


@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = app.root_path+"/project1.db"
    return send_file(path, as_attachment=True)





@app.route('/doneapp')
def done_app():

    deletedata()
    return "True"



@app.route('/Home')
def my_form_post():
    refres = {'test':'0'}
    refres = {'list': []}
    a = datetime.now()

    lis = fun2()
    
    
    refres['list'] = lis
    con = get_db_connection()  
    con.row_factory = sqlite3.Row  

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
            if  t1.hour+6 <= a.hour:
                con.execute('DELETE FROM packageId')
                con.commit()
        else:
            con.execute('DELETE FROM packageId')
            con.commit()

    with sqlite3.connect("database.db") as con:  
        str2 = ''
        # new_list = []
        for i in lis:
            str2 = str2 +'"'+ i+'"'+','
        cur = con.cursor() 
        query = '''SELECT PackageId FROM packageId1 WHERE PackageId in (''' +str2+''')'''
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
                    # print("===in else==="*100)
                    to_append = "('"+i+"','"+str(a)+"','New_added')"
                    if to_append not in insert_rows:
                        insert_rows.append(to_append)
        else:
            for i in lis:
                to_append = "('"+i+"','"+str(a)+"','New_added')"
                if to_append not in insert_rows:
                    insert_rows.append(to_append)
                # insert_rows.append("('"+i+"','"+str(a)+"','New_added')")
        # print("---"*100)
        # print(lis)
        # print("---"*100)
        # print(insert_rows)
        # print("#"*100)
        # print(update_rows)
        if len(insert_rows) > 0:
            values = ', '.join(map(str, insert_rows))
            sql = "INSERT INTO packageId1 VALUES {}".format(values)
            print(sql)
            cur = con.cursor() 
            cur.execute(sql)  
            con.commit()

        if len(update_rows) > 0 :
            values1 = ', '.join(map(str, update_rows))
            sql1 = "UPDATE packageId1 SET  app_status = 'old' WHERE PackageId in ({})".format(values1)
            # print("Update")
            # print("*"*1000)
            # print(sql1)
            cur = con.cursor()
            cur.execute(sql1)  
            con.commit()

    # return render_template('my-form.html',out_data = refres)
    return redirect(url_for('Home2'))

        
@app.route('/cat',methods=['GET','POST'])
def get_cat_data():
    print("in user")
    ref = {'lis':[]}
    user = request.form
    print("hjdsa")
    print(user)
    ref['lis'] = user.getlist('input')

    category = json.dumps(ref)
    return redirect(url_for('Home', category=category))



@app.route('/deductionpage')
def deduction():
    ref = {'test':{}}
    con = get_db_connection()
    cur = con.cursor()
    sql = "SELECT * FROM deduction"
    cur.execute(sql)
    con.commit()
    row1= cur.fetchall() 
    print(row1)
    dic = {}
    for i in row1:
        if i[0] not in dic:
            dic[i[0]] = {}
            dic[i[0]]["reason"] = i[1]
            dic[i[0]]["by"] = i[2]
    ref['test'] = dic
    return render_template('deduction.html', out_data=ref)



@app.route('/')
def Home():
    
    refte = {'output':[],'test':{},'test1':{},"cat":"HOME PAGE","status":{},'url':''}
    lis = get_appids()
    try:
        category = request.args['category'] 
        cat1 = json.loads(category).get('lis')
        url = "category="+str(category)
        refte['url'] = url
    except:
        cat1 = []
    app_data= get_data(lis)
    refte['app_data'] = app_data
    final_lis = []
    if len(cat1)>0:
        for x in lis:
            if app_data.get(x) in cat1:
                final_lis.append(x)
    else:
        final_lis = lis



    refte['output'] = final_lis
    refte['test'] = get_apps_data(final_lis)
    try:
        messages = request.args['messages'] 
        tmp = json.loads(messages)
        refresh = tmp.get('test')
    except:
        refresh = '0'


    refte['test1'] = refresh

    return  render_template('output.html',out_data=refte)



@app.route('/sanil')
def Sanil():
    ref = {'test':{},'app_data':{},'issue_data':{},'name':''}
    data = get_individul('Sanil')
    ref['test'] = data
    ref['app_data'] = get_data(data.keys())
    issue = get_issue_details()
    for i in data:
        ref['issue_data'][i] = {}
        if issue.get(i):
            ref['issue_data'][i]['Issue'] = issue.get(i).get('Issue')
        else:
            ref['issue_data'][i]['Issue'] = "No Issue"
    out = {}

    ref['working'] = working_link()
    ref['name'] = "Sanil"
    # print("IN"*1000)
    # print(ref.get('test'))
    

    return render_template('individual.html',out_data=ref)


@app.route('/hitesh')
def Hitesh():
    ref = {'test':{},'app_data':{},'issue_data':{},"name":'Hitesh'}
    data = get_individul('Hitesh')
    ref['test'] = data
    ref['app_data'] = get_data(data.keys())
    issue = get_issue_details()
    for i in data:
        ref['issue_data'][i] = {}
        if issue.get(i):
            ref['issue_data'][i]['Issue'] = issue.get(i).get('Issue')
        else:
            ref['issue_data'][i]['Issue'] = "No Issue"
    out = {}

    ref['working'] = working_link()
    

    return render_template('individual.html',out_data=ref)


@app.route('/Aniket')
def Aniket():
    ref = {'test':{},'app_data':{},'issue_data':{},"name":'Aniket'}
    data = get_individul('Aniket')
    ref['test'] = data
    ref['app_data'] = get_data(data.keys())
    issue = get_issue_details()
    for i in data:
        ref['issue_data'][i] = {}
        if issue.get(i):
            ref['issue_data'][i]['Issue'] = issue.get(i).get('Issue')
        else:
            ref['issue_data'][i]['Issue'] = "No Issue"
    out = {}

    ref['working'] = working_link()
    

    return render_template('individual.html',out_data=ref)

@app.route('/Jitendra')
def Jitendra():
    ref = {'test':{},'app_data':{},'issue_data':{},"name":'Jitendra'}
    data = get_individul('Jitendra')
    ref['test'] = data
    ref['app_data'] = get_data(data.keys())
    issue = get_issue_details()
    for i in data:
        ref['issue_data'][i] = {}
        if issue.get(i):
            ref['issue_data'][i]['Issue'] = issue.get(i).get('Issue')
        else:
            ref['issue_data'][i]['Issue'] = "No Issue"
    out = {}

    ref['working'] = working_link()
    

    return render_template('individual.html',out_data=ref)


@app.route('/Anirudhh')
def Anirudhh():
    ref = {'test':{},'app_data':{},'issue_data':{},"name":'Anirudhh'}
    data = get_individul('Anirudhh')
    ref['test'] = data
    ref['app_data'] = get_data(data.keys())
    issue = get_issue_details()
    for i in data:
        ref['issue_data'][i] = {}
        if issue.get(i):
            ref['issue_data'][i]['Issue'] = issue.get(i).get('Issue')
        else:
            ref['issue_data'][i]['Issue'] = "No Issue"
    out = {}

    ref['working'] = working_link()
    

    return render_template('individual.html',out_data=ref)




@app.route('/Shraddha')
def Shraddha():
    ref = {'test':{},'app_data':{},'issue_data':{},"name":'Shraddha'}
    data = get_individul('Shraddha')
    ref['test'] = data
    ref['app_data'] = get_data(data.keys())
    issue = get_issue_details()
    for i in data:
        ref['issue_data'][i] = {}
        if issue.get(i):
            ref['issue_data'][i]['Issue'] = issue.get(i).get('Issue')
        else:
            ref['issue_data'][i]['Issue'] = "No Issue"
    out = {}

    ref['working'] = working_link()
    

    return render_template('individual.html',out_data=ref)


@app.route('/Praveen')
def Praveen():
    ref = {'test':{},'app_data':{},'issue_data':{},"name":'Praveen'}
    data = get_individul('Praveen')
    ref['test'] = data
    ref['app_data'] = get_data(data.keys())
    issue = get_issue_details()
    for i in data:
        ref['issue_data'][i] = {}
        if issue.get(i):
            ref['issue_data'][i]['Issue'] = issue.get(i).get('Issue')
        else:
            ref['issue_data'][i]['Issue'] = "No Issue"
    out = {}

    ref['working'] = working_link()
    

    return render_template('individual.html',out_data=ref)

@app.route('/Shreya')
def Shreya():
    ref = {'test':{},'app_data':{},'issue_data':{},"name":'Shreya'}
    data = get_individul('Shreya')
    ref['test'] = data
    ref['app_data'] = get_data(data.keys())
    issue = get_issue_details()
    for i in data:
        ref['issue_data'][i] = {}
        if issue.get(i):
            ref['issue_data'][i]['Issue'] = issue.get(i).get('Issue')
        else:
            ref['issue_data'][i]['Issue'] = "No Issue"
    out = {}

    ref['working'] = working_link()
    

    return render_template('individual.html',out_data=ref)

@app.route('/Deepak')
def Deepak():
    ref = {'test':{},'app_data':{},'issue_data':{},"name":'Deepak'}
    data = get_individul('Deepak')
    ref['test'] = data
    ref['app_data'] = get_data(data.keys())
    issue = get_issue_details()
    for i in data:
        ref['issue_data'][i] = {}
        if issue.get(i):
            ref['issue_data'][i]['Issue'] = issue.get(i).get('Issue')
        else:
            ref['issue_data'][i]['Issue'] = "No Issue"
    out = {}

    ref['working'] = working_link()
    

    return render_template('individual.html',out_data=ref)

@app.route('/Sagar')
def Sagar():
    ref = {'test':{},'app_data':{},'issue_data':{},"name":'Sagar'}
    data = get_individul('Sagar')
    ref['test'] = data
    ref['app_data'] = get_data(data.keys())
    issue = get_issue_details()
    for i in data:
        ref['issue_data'][i] = {}
        if issue.get(i):
            ref['issue_data'][i]['Issue'] = issue.get(i).get('Issue')
        else:
            ref['issue_data'][i]['Issue'] = "No Issue"
    out = {}

    ref['working'] = working_link()
    

    return render_template('individual.html',out_data=ref)


@app.route('/Shrey')
def Shrey():
    ref = {'test':{},'app_data':{},'issue_data':{},"name":'Shrey'}
    data = get_individul('Shrey')
    ref['test'] = data
    ref['app_data'] = get_data(data.keys())
    issue = get_issue_details()
    for i in data:
        ref['issue_data'][i] = {}
        if issue.get(i):
            ref['issue_data'][i]['Issue'] = issue.get(i).get('Issue')
        else:
            ref['issue_data'][i]['Issue'] = "No Issue"
    out = {}

    ref['working'] = working_link()
    

    return render_template('individual.html',out_data=ref)



@app.route('/Raju')
def Raju():
    ref = {'test':{},'app_data':{},'issue_data':{},"name":'Raju'}
    data = get_individul('Raju')
    ref['test'] = data
    ref['app_data'] = get_data(data.keys())
    issue = get_issue_details()
    for i in data:
        ref['issue_data'][i] = {}
        if issue.get(i):
            ref['issue_data'][i]['Issue'] = issue.get(i).get('Issue')
        else:
            ref['issue_data'][i]['Issue'] = "No Issue"
    out = {}

    ref['working'] = working_link()
    

    return render_template('individual.html',out_data=ref)












@app.route('/datapost',methods=['GET','POST'])
def datapost():
    da = {}
    try:
        user = request.form['username']
        url = request.form.get('url')
        ti = request.form.get('time')
        con = get_db_connection()
        checked = "checked"
        # con.execute('DELETE FROM checkedid')
        sql1 = "UPDATE teamdetails SET  checked = '"+str(checked)+"' , done_time = '"+str(ti)+"' WHERE PackageId =  '{}'".format(user)
        print(sql1)
        cur = con.cursor()
        cur.execute(sql1)  
        con.commit()
        da['hello'] = user
    except:
        pass
    return redirect(url_for(url))

@app.route('/datapostdelet',methods=['GET','POST'])
def datapostdel():
    da = {}
    try:
        user = request.form['username']
        # print("find"*10)
        # print(user)
        # print("find"*10)
        con = get_db_connection()
        # checked = "checked"
        # con.execute('DELETE FROM checkedid')
        # id = "'"+user+"'"
        checked = "No"
        ti = "Not yet"
        sql1 = "UPDATE teamdetails SET  checked = '"+str(checked)+"' , done_time = '"+str(ti)+"' WHERE PackageId =  '{}'".format(user)
        print(sql1)
        cur = con.cursor()
        cur.execute(sql1)  
        con.commit()
        da['hello'] = user
    except:
        pass
    return redirect('/')


@app.route('/getissuedata', methods=['GET','POST'])
def get_issue_data():
    print("*"*1008)
    print("in issue")
    print(request.form)
    refres = {}
    if request.method == 'GET':
            pass
    else:
        print(request.form)
        if request.form.get('name'):
            li = request.form['name']
            l2 = request.form.get('app_id')
            url = request.form.get('url')
            con = get_db_connection()
            # con.execute("create table IF NOT EXISTS Issue (PackageId TEXT PRIMARY KEY, Issue TEXT)")
            query = "SELECT Package_name FROM issueeApp WHERE Package_name ="+"'"+l2+"'"
            print(query)
            cur = con.cursor()
            cur.execute(query)
            con.commit()
            rows = cur.fetchall() 
            print(rows)
            print(url)
            # s2 = "('"+l2+"','"+str(li)+"','"+str(url)+"')"
            # print(s2)
            print("A"*100)
            if len(rows) > 0:
                sql1 = "UPDATE issueeApp SET  issue = '"+str(li)+"' WHERE Package_name =  '{}'".format(l2)
                print(sql1)
                cur = con.cursor()
                cur.execute(sql1)  
                con.commit()
                
            else:
                sql = "('"+l2+"','"+str(li)+"')"
                sql2 = "INSERT INTO issueeApp VALUES {}".format(sql)
                print(sql2)
                cur = con.cursor() 
                cur.execute(sql2)  
                con.commit()
            if url == "Home":
                s2 = "('"+l2+"','"+str(li)+"','"+'Himanshu'+"')"
            else:
                s2 = "('"+l2+"','"+str(li)+"','"+str(url)+"')"
            # print(s2)
            sql12 = "INSERT INTO dailyissueeApp VALUES {}".format(s2)
            print(sql12)
            cur = con.cursor() 
            cur.execute(sql12)  
            con.commit()
            checked = "ISSE"
            ti = datetime.now().strftime("%d-%b")
            sql123 = "UPDATE teamdetails SET  checked = '"+str(checked)+"' , done_time = '"+str(ti)+"' WHERE PackageId =  '{}'".format(l2)
            print(sql123)
            cur = con.cursor() 
            cur.execute(sql123)  
            con.commit()
    
    return redirect(url_for(url))






@app.route('/remove')
def remove():
    args = request.args
    print("*"*1000)
    print(args)
    id = args.get('id').split('$')[0]
    name = args.get('id').split('$')[1]
    con = get_db_connection()
    if name == "deduct":
        query = "DELETE  FROM deduction WHERE PackageId = '{}'".format(id)
        cur = con.cursor()
        cur.execute(query)
        con.commit()
        return redirect('/deductionpage')

    query = "DELETE  FROM teamdetails WHERE Assign_to = '{}' AND PackageId = '{}'".format(name,id)
    con = get_db_connection()
    cur = con.cursor()
    cur.execute(query)
    con.commit()
    return redirect('/seedetails')
    


@app.route('/getdata', methods=['GET','POST'])
def get_form_data():
    print("*"*100)
    refres = {}
    if request.method == 'GET':
            return render_template('my-form.html',out_data = refres)
    else:
        print(request.form)
        if request.form.get('Name'):
            name = request.form['Name'].strip()
            appid = request.form.get('app_id').strip()
            url = request.form.get('url')
            url2 = request.form.get('url2')
#     print("$"*1000)
#     print(url2)
#     print("$"*1000)
# comm
    con = get_db_connection()
    if request.form.get('page') == 'deduct':
        li = request.form['app_id'].strip()
        l2 = request.form.get('reason')
        l3 = request.form.get('feedbackby')

        cur = con.cursor()
        Se = "SELECT PackageId from deduction WHERE  packageId = '{}'".format(li)
        cur.execute(Se)
        con.commit()
        rows = cur.fetchall() 

        if len(rows)>0:
            sql1 = "UPDATE deduction SET  reason = '{}' , feedback_by = '{}' WHERE PackageId in ('{}')".format(l2,l3,li)
            print(sql1)
            cur = con.cursor()
            cur.execute(sql1)
            con.commit()
        else:
            print(li)
            print(l2)
            print(l3)
            toadd = "('"+li+"','"+str(l2)+"','"+l3+"')"
            sql = "INSERT INTO deduction VALUES {}".format(toadd)
            print(sql)
            cur = con.cursor() 
            cur.execute(sql)  
            con.commit()

        return redirect(url_for('deduction'))

    # con = get_db_connection()
    value = name
    value1 = appid
    a = datetime.now()

    cur = con.cursor()
    S = "SELECT PackageId from packageId WHERE  packageId = '{}'".format(value1)
    cur.execute(S)
    con.commit()
    rows = cur.fetchall() 


    if len(rows)>0:
        sql1 = "UPDATE packageId SET  assign_to = '{}' WHERE PackageId in ('{}')".format(value,value1)
        print(sql1)
        cur = con.cursor()
        cur.execute(sql1)
        con.commit()
    else:
        toadd = "('"+value1+"','"+str(a)+"','New_added','"+value+"')"
        sql = "INSERT INTO packageId VALUES {}".format(toadd)
        print(sql)
        cur = con.cursor() 
        cur.execute(sql)  
        con.commit()


    sql = "('"+value1+"','"+str(a)+"',"+"'"+value+"',"+"'Not yet','No')"
    print(sql)
    sql = "INSERT INTO teamdetails VALUES {}".format(sql)
    print(sql)
    cur = con.cursor() 
    cur.execute(sql)  
    con.commit()
    # print(url)
    # print("lakjsdalk"*100)
    if url:
        return redirect(url_for(url))
    else:
        return redirect('/')





@app.route('/d')
def refresh():
    himanshudata.refresh()
    refres = {'test':'1'}
    messages = json.dumps(refres)
    return redirect(url_for('Home', messages=messages))


@app.route('/details')
def details():
    args = request.args
    try:
        id2 = args.get('id').split('_')[0]
        url = "asdg"
    except:
        id2 = args.get('id')
    print(args)
    print("*"*100)
    out = {"package":id2}
    que1  ="SELECT * FROM 'updatedetails' WHERE Package_name = '"+id2+"'"
    con = sqlite3.connect("project1.db")  
    con.row_factory = sqlite3.Row
    cur = con.cursor()  
    cur.execute(que1)
    row1 = cur.fetchall()
    updated_list = [dict(ix) for ix in row1]
    if updated_list:
        out['id'] = updated_list
    else:
        out['id'] = [{}]

    # if url:
    #     return render_template('detalsper.html',out_data=out)
    # else:
    return render_template('details.html',out_data=out)
    

@app.route('/seedetails')
def teamdeatils():
    ref = {'test':{},'li':[],'test2':{},'li2':[]}
    dic,dic1,dic2 = get_individul_data()
    ref['test'] = dic
    ref['test2'] = dic1
    ref['test3'] = dic2
    lis = dic.keys()
    l = list(lis)
    lis2 = dic1.keys()
    l2 = list(lis2)
    lis3 = dic2.keys()
    l3 = list(lis3)
    # l = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    n = 3
    x = [l[i:i + n] for i in range(0, len(l), n)]

    ref['li'] = x
    z = [l3[i:i + n] for i in range(0, len(l3), n)]
    print("Ac"*100)
    print(x)
    print("Ac"*100)
    ref['li3'] = z
    y = [l2[i:i + n] for i in range(0, len(l2), n)]

    ref['li2'] = y
    return render_template('detalsper.html', out_data=ref)

@app.route('/issue')
def issue():
    args = request.args
    out = {"package":args.get('id')}
    que1  ="SELECT * FROM 'issueApp' WHERE Package_name = '"+args.get('id')+"'"
    con = sqlite3.connect("database.db")  
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






@app.route('/_get_ajax_data/')
def get_ajax_data():
    data = {"hello": "world"}
    response = jsonify(data)
    response.cache_control.max_age = 60 * 60 * 24  # 1 day (in seconds)
    return response  


if __name__ == '__main__':
  
    app.run(debug = True)
