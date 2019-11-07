#new_gallery.py

import cgi
import pymysql
import database_handler


def main():
    form = cgi.FieldStorage()

    gallery_name = ''
    gallery_description = ''

    if ( form.getvalue('gal_name') ):
        gallery_name = form.getvalue('gal_name')
        gallery_name = gallery_name.lower()
    if ( form.getvalue('gal_description') ):
        gallery_description = form.getvalue('gal_description')
        gallery_description = gallery_description.lower()

    print("""
    <!Doctype html>
    <html lang='en'>
    <head>
        <meta charset="UTF-8"/>
        <meta name='viewport' content='width=device-width, initial-scale=1.0' />
        <meta http-equiv='X-UA-Comptatible' content='ie=edge'/>

        <title>Gallery</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
        <link rel="stylesheet" href="css/style.py">
    </head>
    """)

    if (gallery_name == '' ):
        print("""
            <body>
                <h1>new_gallery.py 33: Error! Please make sure name information is filled out and try again</h1>
            </body>
            """)
    else:
        database = database_handler.initialize()
        if ( database == -1 ):
            print("new_gallery.py: There was an error retrieving the database.")

        cursor = database.cursor()

        ##Check if the Gallery Already exists
        query = "SELECT gallery_id from gallery WHERE name = '" + gallery_name + "'"
        cursor.execute(query)
        response = cursor.fetchone()
        if ( response != None ):
            print("The database with name %s already exists" % gallery_name )
            #return 0
        else:
            #Get new gallery ID
            query = "SELECT MAX(gallery_id) FROM gallery"
            cursor.execute(query)
            print("Result: " + str(cursor.fetchone()))
            response = cursor.fetchone()
            if ( response == None ):
                gallery_id = 0
            else:
                gallery_id = int(response[0]) + 1

            query = "INSERT IGNORE INTO gallery(gallery_id, name, description) VALUES(%s, %s, %s)"
            values = (gallery_id, gallery_name, gallery_description)
            cursor.execute(query, values)
            database.commit()
            database.close()
    print( """
            <script>
                window.close()
            </script>
    """)

def insert_new_gallery( name, description ):
        database = database_handler.initialize()
        if ( database == -1 ):
            print("new_gallery.py: There was an error retrieving the database.")
            return 0
        cursor = database.cursor()
        #Get new gallery ID
        query = "SELECT MAX(gallery_id) FROM gallery"
        cursor.execute(query)
        response = cursor.fetchone()
        if ( response == None ):
            gallery_id = 0
        else:
            gallery_id = int(response[0]) + 1
        query = "INSERT IGNORE INTO gallery(gallery_id, name, description) VALUES(%s, %s, %s)"
        values = (gallery_id, gallery_name, gallery_description)
        cursor.execute(query, values)
        database.commit()
        database.close()
        return 0

if __name__ == '__main__':
    main()
