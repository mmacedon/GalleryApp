#new_detail.py
import cgi
import pymysql
import database_handler

def insert_new_detail(image_id):

    database = database_handler.initialize()
    if ( database == -1 ):
        print("new_detail.py insert_new_detail(): There was an error linking database.")
    else:
        cursor = database.cursor()
        query = "SELECT MAX(detail_id) FROM detail"
        cursor.execute(query)
        response = cursor.fetchone()
        if (response[0] == None):
            detail_id = 0
        else:
            detail_id = int(response[0]) + 1

        #insert into database
        query = "INSERT IGNORE INTO detail(detail_id, image_id, year, type, width, height, location, description) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (str(detail_id), str(image_id), '', '', '', '', '', '')
        cursor.execute(query, values)
        database.commit()
    database.close()
    return detail_id
