#--*--coding:utf-8--*--

import  MySQLdb

def connection(select,sql):
     connection = MySQLdb.connect(host=u'127.0.0.1', user=u'root', passwd=u'123456', db=u'kbook', charset=u'utf8',
                             cursorclass=MySQLdb.cursors.DictCursor)
     cursor = connection.cursor()
     cursor.execute(sql)
     if select==1:
        row = cursor.fetchall()
     elif select==2:
        row = cursor.fetchone()
     return  row