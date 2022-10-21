

import sqlite3

def get_db_connection():
    conn = sqlite3.connect('project1.db')
    conn.execute("create table IF NOT EXISTS workinglinks (PackageId TEXT PRIMARY KEY)")  
    conn.execute("create table IF NOT EXISTS packageId (PackageId TEXT PRIMARY KEY,time TEXT NOT NULL,app_status TEXT, assign_to TEXT )")  
    conn.execute("create table IF NOT EXISTS teamdetails (PackageId TEXT , Assign_time TEXT NOT NULL, Assign_to TEXT, done_time TEXT , checked TEXT )")  
    conn.execute("create table IF NOT EXISTS donedetails (PackageId TEXT , done_by TEXT, done_time TEXT)")  
    conn.execute("create table IF NOT EXISTS deduction (PackageId TEXT , reason TEXT, feedback_by TEXT)")  

    # conn.execute('DELETE FROM teamdetails')
    # conn.commit()
    return conn


# get_db_connection()