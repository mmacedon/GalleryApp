#modify_image.py
import cgi
import database_handler
import pymysql
import new_artist

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

    imageTitle = ''
    imageNewTitle = ''
    imageLink = ''
    imageGallery = ''
    imageArtist = ''
    imageDetail = ''
    success = 0
    form = cgi.FieldStorage()

    if ( form.getvalue('imageTitle') ):
        imageTitle = form.getvalue('imageTitle')
        imageTitle = imageTitle.lower()
    if ( form.getvalue('imageNewTitle') ):
        imageNewTitle = form.getvalue('imageNewTitle')
        imageNewTitle = imageNewTitle.lower()
    if ( form.getvalue('imageLink') ):
        imageLink = form.getvalue('imageLink')
    if ( form.getvalue('imageGallery') ):
        imageGallery = form.getvalue('imageGallery')
        imageGallery = imageGallery.lower()
    if ( form.getvalue('imageArtist') ):
        imageArtist = form.getvalue('imageArtist')
        imageArtist = imageArtist.lower()
    if ( form.getvalue('imageDetail') ):
        imageDetail = form.getvalue('imageDetail')
        imageDetail = imageDetail.lower()

    imageDetail = ''
    if ( imageTitle == ''):
        print( """
            <body>
                <h1>modify_image.py main(): Need to input name fields.
            </body>
        """)
        print( form )
    else:
        database = database_handler.initialize()
        if ( database == -1 ):
            print("modify_image.py main(): There was an error retrieving the database.")

        cursor = database.cursor()

        #Get both image ids
        query = "SELECT image_id FROM image WHERE title = '" + imageTitle + "'"
        cursor.execute(query)
        response = cursor.fetchone()

        if ( imageNewTitle == '' ):
            query = "SELECT title FROM image WHERE title = '" + imageTitle + "'"
            cursor.execute(query)
            result = cursor.fetchone()
            imageNewTitle = result[0]
        query = "SELECT image_id FROM image WHERE title = '" + imageNewTitle + "'"
        cursor.execute(query)
        response_2 = cursor.fetchone()

        if ( imageLink == '' ):
            query = "SELECT link FROM image WHERE title = '" + imageTitle + "'"
            cursor.execute(query)
            result = cursor.fetchone()
            imageLink = result[0]

        #Get the gallery id
        if (  imageGallery == ''):
            query = "SELECT gallery_id FROM image WHERE title = '" + imageTitle + "'"
            cursor.execute(query)
            result = cursor.fetchone()
            gallery_id = int(result[0])
        else:
            query = "SELECT gallery_id FROM gallery WHERE name = '" + imageGallery + "'"
            cursor.execute(query)
            check = cursor.fetchone()
            if ( check == None ):
                print("Error: The gallery does not exist. Create the gallery first")
                success = -1
        #Get the Artist Id:
        if ( imageArtist == '' ):
            query = "SELECT artist_id FROM image WHERE title = '" + imageTitle + "'"
            cursor.execute(query)
            result = cursor.fetchone()
            artist_id = int(result[0])
        else:
            query = "SELECT artist_id FROM artist WHERE name = '" + imageArtist + "'"
            cursor.execute(query)
            check = cursor.fetchone()
            if ( check == None ):
                print("modify_image.py main(): Artist does not exist. Adding new Artist.")
                artist_id = new_artist.insert_new_artist(imageArtist)
                if ( artist_id != 0 ):
                    print("modify_image.py main(): Artist added successfully")
                else:
                    print("modify_image.py main(): Error Adding Artist")
            else:
                artist_id = int ( check[0] )

        #Get the detail ID
        if ( imageDetail == '' ):
            query = "SELECT detail_id FROM image WHERE title = '" + imageTitle + "'"
            cursor.execute(query)
            result = cursor.fetchone()
            detail_id = int(result[0])
        else:
            query = "SELECT detail_id from detail WHERE image_id = '" + int(response[0]) + "'"
            cursor.execute(query)
            check = cursor.fetchone()
            if ( check == None ):
                print("modify_image.py main(): The image details do not exist")
                detail_id = new_detail.insert_new_detail(image_id)
            else:
                detail_id = int(check[0])

        if ( response == None ):
            print("modify_image.py main(): The image does not exist")
        else:
            image_id = int ( response[0] )
            second_image_id = int ( response_2[0] )

            if ( image_id == second_image_id ):
                query = 'UPDATE image SET title = %s, link = %s, gallery_id = %s, artist_id = %s, detail_id = %s WHERE image_id = %s'
                values = (imageNewTitle, imageLink, gallery_id, artist_id, detail_id, image_id )
                cursor.execute(query, values)
                database.commit()
            else:
                print("modify_image.py main(): There is another image with name %s" % imageNewTitle)
        database.close()
    print("""
            <script>
                window.close()
            </script>
          """)
    return 0

if __name__ == '__main__':
    main()
