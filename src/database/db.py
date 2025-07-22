import pymysql

def get_connection():
    return pymysql.connect(
        host="100.124.58.32",
        user="root",
        password="",
        database="db_ai",
        cursorclass=pymysql.cursors.DictCursor
    )
