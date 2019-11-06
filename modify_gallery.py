#Modify_Gallery
import cgi
import database_handler
import pymysql

def main():

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

    gallery_name = ''
    gallery_new_name = ''
    gallery_new_description = ''

    form = cgi.FieldStorage()

    if ( form.getvalue('galleryName') ):
        gallery_name = form.getvalue('galleryName')
        gallery_name = gallery_name.lower()
    if ( form.getvalue('galleryNewName') ):
        gallery_new_name = form.getvalue('galleryNewName')
        gallery_new_name = gallery_new_name.lower()
    if ( form.getvalue('galleryDescription') ):
        galleryDescription = form.getvalue('galleryDescription')
        galleryDescription = galleryDescription.lower()

    if ( (gallery_new_name == '') or ( gallery_name == '' ) ):
        print("""
            <body>
                <h1>modify_gallery.py main(): Need to input gallery name fields.
            </body>
        """)
        print(form)
    else:
        database = database_handler.initialize()
        if ( database == -1 ):
            print("modify_gallery.py main(): There was an error retrieving the database.")

        cursor = database.cursor()

        query = "SELECT gallery_id FROM gallery WHERE name = '" + gallery_name + "'"
        cursor.execute(query)
        response = cursor.fetchone()

        query = "SELECT gallery_id FROM gallery where name = '" + gallery_new_name + "'"
        cursor.execute(query)
        response_2 = cursor.fetchone()

        if ( response == None ):
            print("modify_gallery.py main(): The gallery does not exist!")
        elif ( response_2 != None ):
            print("modify_gallery.py main(): There is already a gallery with name %s" % gallery_new_name )
        else:
            gallery_id = int(response[0])
            query = "UPDATE gallery SET name = %s, description = %s WHERE gallery_id = %s"
            values = (gallery_new_name, galleryDescription, gallery_id)
            cursor.execute(query, values)
            database.commit()
        database.close()
    print("""
        <script>
            window.close()
        </script>
    """)
    return 0

if __name__ == '__main__':
    main()
