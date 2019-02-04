import numpy as np
import pandas as pd
import pymysql
import sqlalchemy
import logging
import traceback
import datetime
import send_email

"""
All sensitive variables (file path, db, password, host, user, schema, sheet_names)
have been stripped to protect confidentiality. This script was ultimately placed 
on a VM where it was scheduled with chron to run twice a week.
"""

#List sheet names
sheet_names = ['Sheet1',
               'Sheet2',
               'Sheet3',
               'Sheet4',
               'Sheet5',
               'Sheet6',
               'Sheet7',
               'Sheet8']

def etlscript(sheet_names):
    #Create blank dictionary for the dataframes (d)
    d = {}
    print('Reading data')
    data = (pd.ExcelFile('File Path'))

    print('Assigning sheets to dataframes')
    for sheet in sheet_names:
        d[sheet] = pd.DataFrame()
        sheetdata = (pd.read_excel(data, sheet))
        d[sheet] = d[sheet].append(sheetdata)

    print('Connecting to database')
    #Input Connection info
    db = 'dbName'
    password='password'
    user = 'user'
    host='host'
    connection = pymysql.connect(
                                 host=host,
                                 user = user,
                                 password=password,
                                 db = db
                                 )
    engine = sqlalchemy.create_engine('mysql+pymysql://'+user+':'+password+'@'+host+':3306/'+db)

    print('Truncating existing data')
    with connection.cursor() as cursor:
    #Run the stored procedure that clears all data
        sql = "Call TruncateTables"
        cursor.execute(sql)
    
    connection.close()

    print('Inserting new data')
    for sheet in sheet_names:
        print('Inserting '+sheet)
        d[sheet].to_sql(name=sheet,
                        con=engine,
                        schema = 'schema',
                        if_exists='append',
                        index=False)

    print('Done!')

try:
    etlscript(sheet_names)
except Exception as x:
    print(traceback.format_exc())
    send_email.send_error_message(traceback.format_exc())
