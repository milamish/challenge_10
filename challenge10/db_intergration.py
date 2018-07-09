from flask import *
from functools import wraps
import datetime
import pymysql
import jwt
import time


app=Flask(__name__)
app.config ['SECRET_KEY']='mish'

def tokens(k):
    @wraps(k)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message' : 'Token is missing'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])

        except:
            return jsonify({'message' : 'Token is invalid'}), 403

        return k(*args, **kwargs)
    return decorated

@app.route("/home",methods=['GET'])
def home():
    return jsonify({"message":"you are home"})

@app.route("/users", methods=['POST','GET'])
def users():
    Name= request.get_json()['Name']
    Email_adress= request.get_json()['Email_adress']
    Password= request.get_json()['Password']
    Username=request.get_json()['Username']
    User_type=request.get_json()['User_type']
    User_ID=request.get_json()['User_ID']
    Date =request.get_json()['Date']
    
    try:
        connection = pymysql.connect(host ='localhost',user='root',password='',db='flask_api')
        with connection.cursor() as cursor:
            sql="INSERT INTO `users`(`Name`,`Email_adress`,`Password`,`Username`,`User_type`,`User_ID`,`Date`) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            try: 
                cursor.execute("SELECT * FROM `users` WHERE `Username`=%s;",Username)
                if cursor.fetchone() is not None:
                    return jsonify({"message":"Username taken"})
                else: 
                    cursor.execute(sql,(Name,Email_adress,Password,Username,User_type,User_ID,Date))
            except:
                return jsonify({"message":"oops!"})
        connection.commit()
    finally:
        connection.close()
    return jsonify({"message":"registered!"})

@app.route("/login",methods=['POST','GET'])
def login():
    Username= request.get_json()['Username']
    Password=request.get_json()['Password']
    try:
        connection = pymysql.connect(host ='localhost',user='root',password='',db='flask_api')
        with connection.cursor() as cursor:
            sql_log="SELECT * FROM `users` WHERE `Username` LIKE '"+Username+"' and `Password` LIKE '"+Password+"'"
            try:
                cursor.execute(sql_log)
                result=cursor.fetchone()
                if result is None :
                    return jsonify({"message":"user not found"})
                else:
                    token=jwt.encode({'Username':Username,'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},app.config['SECRET_KEY'])
                    #if Password == each[4] and Username==each[2]:
                    return jsonify({"message":"succesfuly logged in",'token':token.decode ('UTF-8')})
                        #return jsonify({"message":"you are logged in"})
                  
            except:
                    return jsonify({"message":"check your login details"})
        connection.commit()
    finally:
        connection.close()
   

@app.route("/user_comments", methods=['POST','GET'])
@tokens
def comments():
    Date = request.get_json()['Date']
    comment = request.get_json()["comment"]
    User_ID = request.get_json()["User_ID"]
    
    try:
        connection = pymysql.connect(host ='localhost',user='root',password='',db='flask_api')
        with connection.cursor() as cursor:
            sql_com= "INSERT INTO `user_comments`(`Date`,`comment`,`User_ID`) VALUES(%s,%s,%s)"
            try: 
                cursor.execute(sql_com,(Date,comment,User_ID))
            except:
                return jsonify({"message":"oops!"})
        connection.commit()
    finally:
        connection.close()
        return jsonify(comment)

@app.route("/Admin", methods=['POST','GET'])
@tokens
def Admin():
    Admin_ID = request.get_json()['Admin_ID']
    User_ID = request.get_json()["User_ID"]
    
    try:
        connection = pymysql.connect(host ='localhost',user='root',password='',db='flask_api')
        with connection.cursor() as cursor:
            sql_admin= "INSERT INTO `admin`(`Admin_ID`,`User_ID`) VALUES(%s,%s)"
            try: 
                cursor.execute(sql_admin,(Admin_ID,User_ID))
            except:
                return jsonify({"message":"oops!"})
        connection.commit()
    finally:
        connection.close()
        return jsonify({"message":"new admin registered"})

@app.route("/delete_user/<int:User_ID>",methods=['DELETE','POST'])
@tokens
def delete_user(User_ID):
    Username = request.get_json()['Username']
    try:
        connection=pymysql.connect(host='localhost',user='root',password='',db='flask_api')
        with connection.cursor() as cursor:
            sql_del="DELETE FROM `users` WHERE `User_ID`= "+str(User_ID) +" and `users`.`Username`="+str(Username[len(Username)-1])+ ""
            try:
                cursor.execute(sql_del)
                return jsonify({"message":"user succesfully deleted"})
            except:
                return jsonify({"message":"unable to delete user"})
        connection.commit()
    finally:
        connection.close()

@app.route("/delete_comment/<int:comment_ID>",methods=['DELETE','POST'])
@tokens
def delete_comment(comment_ID):
    User_ID=request.get_json()['User_ID']
    try:
        connection=pymysql.connect(host='localhost',user='root',password='',db='flask_api')
        with connection.cursor() as cursor:
                sql="DELETE FROM `user_comments` WHERE `user_comments`.`comment_ID` = "+str(comment_ID)+" and `user_comments`.`User_ID`="+str(User_ID[len(User_ID)-1])+""
                try:
                    cursor.execute(sql)
                except:
                    return jsonify({"message": "unable to delete comments"})
        connection.commit()
    finally:
        connection.close()
    return jsonify({"message": "comment succesfully deleted"})

@app.route("/read_comments",methods=['POST','GET'])
def read_comments():
    try:
        connection=pymysql.connect(host='localhost',user='root',password='',db='flask_api')
        with connection.cursor() as cursor:
            sql_read="SELECT * FROM `User_comments`"
            try:
                cursor.execute(sql_read)
                result= cursor.fetchall()
                return jsonify(result)
                row=cursor.fetchall()
                for row in result:
                    row=cursor.fetchall()
                    comment=row[0]
                    comment_ID=row[1]
                    return jsonify(str(row[0]) + "\n\n" + "\t\t" + row[1] +"\n\n" + row[2] + "\n\n" + row[3])
            except:
                return jsonify({"message":"unable to fetch data"})
            connection.commit()
    finally:
        connection.close()  

@app.route("/read_users",methods=['POST','GET'])
def read_users():
    try:
        connection=pymysql.connect(host='localhost',user='root',password='',db='flask_api')
        with connection.cursor() as cursor:
            sql_read_user="SELECT * FROM `Users`"
            try:
                cursor.execute(sql_read_user)
                result= cursor.fetchall()
                return jsonify(result)
                row=cursor.fetchall()
                for row in result:
                    row=cursor.fetchall()
                    return jsonify(str(row[0]) + "\n\n" + "\t\t" + row[1] +"\n\n" + row[2] + "\n\n" + row[3])
            except:
                return jsonify({"message":"unable to fetch data"})
            connection.commit()
    finally:
        connection.close()  



if __name__=="__main__":
    app.run(debug=True)