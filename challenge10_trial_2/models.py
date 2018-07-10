from flask import *
import pymysql

def table():
    connection = pymysql.connect(host ='localhost',user='root',password='',db='flask_api')
    with connection.cursor() as cursor:
        cursor.execute()
        results = cursor.fetchone()
        if result is not None:
            pass
        else:    
            cursor.execute("CREATE TABLE `admin` (`Admin_ID` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,`User_ID` int(50) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=latin1;")
            cursor.execute("CREATE TABLE `users` (`User_ID` int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,`Name` char(100) NOT NULL,`Username` varchar(100) NOT NULL,`Email_adress` varchar(100) NOT NULL,`Password` varchar(50) NOT NULL,`User_type` char(50) NOT NULL,`Date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP) ENGINE=InnoDB DEFAULT CHARSET=latin1;")
            cursor.execute("CREATE TABLE `user_comments` (`comment_ID` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY ,`Date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,`comment` text NOT NULL,`User_ID` int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=latin1;")
    connection.commit()
    connection.close()