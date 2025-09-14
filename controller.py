from flaskext.mysql import MySQL
from flask import Flask
import uuid
import logging

class Controller:
    def __init__(self):
        self.app = Flask(__name__)

        logging.basicConfig(level=logging.DEBUG)

        self.mysql=MySQL()

        self.app.config['MYSQL_DATABASE_HOST']='localhost'
        self.app.config['MYSQL_DATABASE_USER']='root'
        self.app.config['MYSQL_DATABASE_PASSWORD']='123'
        self.app.config['MYSQL_DATABASE_DB']='user_db'

        self.mysql.init_app(self.app)

    def loginQuery(self, username, password):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from user_tb where username='"+username+"' and password='"+password+"'")

        data = cursor.fetchall()

        if(len(data)>0):
            hash=str(uuid.uuid4())
            cursor.execute("update user_tb set token = '"+hash+"' where user_id="+str(data[0][0]))
            conn.commit()

            cursor.close()
            conn.close()
        else:
            return None

        

        return hash
    
    def tokenLogin(self, token):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("select * from user_tb where token='"+token+"'")
        data = cursor.fetchall()

        cursor.close()
        conn.close()

        if(len(data)>0):
            return True
        else:
            return False
        
    def deleteData(self, id):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("delete from user_tb where user_id="+id)
        conn.commit()

        cursor.close()
        conn.close()
        return True
    
    def getData(self):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        column="user_id, username, password, role, is_enable"
        cursor.execute("select "+column+" from user_tb")
        data = cursor.fetchall()
        arr=column.split(",")
        counter=0
        mainCounter=int(len(data))
        dataDict={}
        dataList=list()
        while(counter<=5 and mainCounter>0):
            dataDict[arr[counter].strip()]=data[mainCounter-1][counter]
            counter+=1
            if (counter>=5):
                dataList.append(dataDict)
                dataDict={}
                if (mainCounter>0):
                    counter=0
                    mainCounter-=1

        cursor.close()
        conn.close()

        if(len(dataList)>0):
            return dataList
        else:
            return None
        
    def insertData(self, username, password, is_admin):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("insert into user_tb (username, password, role, is_enable) values ('"+username+"', '"+password+"', '"+str(is_admin)+"', '"+str(1)+"')")
        conn.commit()

        cursor.close()
        conn.close()

        return True
    
    def updateData(self, key, value, id):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        self.app.logger.info("update user_tb set "+key+"="+value+" where user_id="+str(id))
        cursor.execute("update user_tb set "+key+"='"+value+"' where user_id="+str(id))
        conn.commit()

        cursor.close()
        conn.close()

        return True