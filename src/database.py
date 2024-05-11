import mysql.connector

class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(host='localhost', user="root", password="FOokVoyspOurjy1", database='book_store')
        self.mycursor = self.conn.cursor()

    def commit(self):
        try:
            self.conn.commit()
            return True
        except mysql.connector.Error as err:
            print(f"There was an error occured: {err}")
            return False

    def close_connection(self):
        self.mycursor.close()
        self.conn.close()
