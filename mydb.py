import mysql.connector 

def checkUser(username,pwd):
    try:
        #Note: all the information written in <...> should be updated with your own remote or local mysql credentials.

        conn = mysql.connector.connect(host='<host>', user='<username>', password='<password>', database='<database>')
        cursor = conn.cursor()
        sql = "SELECT * FROM users WHERE user = %s AND pwd = %s"
        cursor.execute(sql, (username,pwd))
        row = cursor.fetchone()
        if row is not None:
            return [True,row]
        else:
            return [False]
    except mysql.connector.Error as err:
        print(err)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()