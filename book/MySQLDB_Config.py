#--*--coding:utf-8--*--

import  MySQLdb

def connection(select,sql):
     connection = MySQLdb.connect(host='127.0.0.1', user='root', passwd='18525350524Yrs', db='book', charset='utf8',
                             cursorclass=MySQLdb.cursors.DictCursor)
     cursor = connection.cursor()
     cursor.execute(sql)
     if select==1:
        row = cursor.fetchall()
     elif select==2:
        row = cursor.fetchone()
     return  row