#delete.py
import pymysql
import database_handler
import cgi

def delete_gallery( gallery_name ):
    database = database_handler.initialize()
    if ( database == -1 ):
        print("delete.py delete_gallery(): Error linking database")
        return -1

    #Check if the database exists
    cursor = database.cursor()
    query = "SELECT gallery_id FROM gallery WHERE name = '" + gallery_name + "'"
    cursor.execute(query)
    response = cursor.fetchone()
    if ( response == None ):
        print("The gallery does not exist")
        return -1
    else:
        gallery_id = int(response[0])

    query = "Delete from gallery WHERE name = '" + gallery_name + "'"
    cursor.execute(query)
    print("Gallery Successfully Deleted. Deleting all images in gallery")


    query = "SELECT image_id FROM image WHERE gallery_id = " + str(gallery_id)
    cursor.execute(query)
    response = cursor.fetchall()
    print(response)
    ids = []
    for i in range(len(response)):
        ids.append(int(response[i][0]))
    print(ids)
    for i in range( len(ids) ):
        query = "Delete from detail WHERE image_id = " + str(ids[i])
        cursor.execute(query)

    query = "Delete from image WHERE gallery_id = " + str(gallery_id)
    cursor.execute(query)

    database.commit()
    database.close()
    return 0

def delete_image ( image_name ):
    database = database_handler.initialize()
    if ( database == -1 ):
        print("delete.py delete_image(): Error linking database")

    cursor = database.cursor()
    query = "SELECT image_id FROM image WHERE title = '" + image_name + "'"
    cursor.execute(query)
    response = cursor.fetchone()
    if ( response == None ):
        print("delete.py delete_image(): There is no image with name %s" % image_name)
    else:
        image_id = int(response[0])
        query = "DELETE FROM image WHERE title = '" + image_name + "'"
        cursor.execute(query)
        query = "DELETE FROM detail WHERE image_id = " + str(image_id)
        cursor.execute(query)

    database.commit()
    database.close()
    return 0

def delete_artist( artist_name ):
    database = database_handler.initialize()
    if ( database == -1 ):
        print("delete.py delete_image(): Error linking database")

    cursor = database.cursor()
    query = "SELECT artist_id FROM artist WHERE name = '" + artist_name + "'"
    cursor.execute(query)
    response = cursor.fetchone()
    if ( response == None ):
        print("delete.py delete_artist(): There is no artist with name %s" % artist_name)
    else:
        artist_id = int(response[0])
        query = "DELETE FROM artist WHERE name = '" + artist_name + "'"
        cursor.execute(query)
        #Need to update all the image tables
        query = "UPDATE image SET artist_id = -1 WHERE artist_id = %s"
        values = (artist_id)
        cursor.execute(query, values)
    database.commit()
    database.close()
    return 0

def main():

    gallery_name = ''
    image_name = ''
    artist_name = ''

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

    form = cgi.FieldStorage()

    if ( form.getvalue('delete_gallery') ):
        gallery_name = form.getvalue('delete_gallery')
        gallery_name = gallery_name.lower()
    if ( form.getvalue('delete_image') ):
        image_name = form.getvalue('delete_image')
        image_name = image_name.lower()
    if ( form.getvalue('delete_artist') ):
        artist_name = form.getvalue('delete_artist')
        artist_name = artist_name.lower()

    if ( gallery_name != '' ):
        success = delete_gallery(gallery_name)
    if ( image_name != '' ):
        delete_image(image_name)
    if ( artist_name != '' ):
        delete_artist(artist_name)

    print("<script>window.close()</script>")
    return 0

if __name__ == '__main__':
    main()
