#new_image.py
import cgi
import database_handler
import new_artist
import new_gallery
import new_detail
import pymysql

def main():
    i_name = ''
    i_link = ''
    i_artist = ''
    i_gallery = ''

    FORM = cgi.FieldStorage()

    if ( FORM.getvalue('name') ):
        i_name = FORM.getvalue('name')
        i_name = i_name.lower()
    if ( FORM.getvalue('link') ):
        i_link = FORM.getvalue('link')
    if ( FORM.getvalue('artist') ):
        i_artist = FORM.getvalue('artist')
        i_artist = i_artist.lower()
    if ( FORM.getvalue('gallery') ):
        i_gallery = FORM.getvalue('gallery')
        i_gallery = i_gallery.lower()

        print( """
            <!Doctype html>
            <html lang='en'>
            <head>
                <meta charset="UTF-8"/>
                <meta name='viewport' content='width=device-width, initial-scale=1.0' />
                <meta http-equiv='X-UA-Comptatible' content='ie=edge'/>

                <title>Gallery</title>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
                <link rel="stylesheet" href="css/style.py">
            </head>""")

    if ( (i_name == '') or (i_link == '')  or (i_artist == '') or (i_gallery == '')):
        print("""
            <body>
                <h1>Image.py: Error! Please make sure all information is filled out and try again</h1>
                console.log(%s)
            </body>
        """ % FORM)
    else:
        database = database_handler.initialize()
        if ( database == -1 ):
            print("new_image.py: There was an error retrieving the database.")
            return -1
        cursor = database.cursor()

        #Check if the Image already exists:
        query = "SELECT image_id FROM image WHERE title = '" + i_name + "'"
        cursor.execute(query)
        if ( len(cursor.fetchall()) > 0 ):
            print("An image with title %s already exists" % i_name)
        else:
            #Get the New Image ID:
            query = "SELECT MAX(image_id) FROM image"
            cursor.execute(query)
            response = cursor.fetchone()
            if ( response[0] == None ):
                image_id = 0
            else:
                image_id = int(response[0]) + 1

            #Get the Gallery:
            query = ("SELECT gallery_id FROM gallery WHERE name = '" + i_gallery + "'")
            cursor.execute(query)
            response = cursor.fetchone()
            if ( response == None ):
                print("Error! The Name Typed in is Not Found in the Gallery.")
                print("Please create the gallery first")
                return -1
            else:
                gallery_id = int(response[0])

                #Get the Artist ID:
                query = "SELECT artist_id FROM artist WHERE name = '" + i_artist + "'"
                cursor.execute(query)
                response = cursor.fetchone()
                if ( response == None ):
                    print("Artist does not exist. Adding Artist")
                    artist_id = new_artist.insert_new_artist(i_artist)
                    if ( artist_id != 0 ):
                        print("Artist added Successfully")
                    else:
                        print("Error Adding Artist.")
                else:
                    artist_id = int(response[0])

                #GET detail ID
                query = "SELECT detail_id FROM detail WHERE image_id = '" + str(image_id) + "'"
                cursor.execute(query)
                response = cursor.fetchone()
                if ( response == None ):
                    detail_id = new_detail.insert_new_detail(image_id)
                    if ( detail_id != 0 ):
                        print("Detail Added Successfully")
                    else:
                        print("Something went wrong")
                else:
                    detail_id = int(response[0])
                query = "INSERT INTO image(image_id, title, link, gallery_id, artist_id, detail_id) VALUES(%s, %s, %s, %s, %s, %s)"
                values = (image_id, i_name, i_link, gallery_id, artist_id, detail_id)
                cursor.execute(query, values)
                database.commit()
        database.close()

        print("""
            <script>
                window.close()
            </script>
            """)

if __name__ == '__main__':
    main()
