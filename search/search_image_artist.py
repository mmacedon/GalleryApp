#Search_image_artist.py
import cgi
import pymysql
import format
import database_handler

def main():
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
    </head>
    """)

    image_artist = ''

    form = cgi.FieldStorage()

    if ( form.getvalue('artist_name') ):
        image_artist = form.getvalue('artist_name')
        image_artist = image_artist.lower()

    if ( image_artist == '' ):
        print("search_image_artist.py main(): Error! Need to input field.")
        return 0

    print("""
        <body>
            <h1> Image Results by %s </h1>
        """ % image_artist)

    database = database_handler.initialize()
    if ( database == -1 ):
        print("search_image_artist.py main(): Error linking database.")
        return 0
    cursor = database.cursor()
    query = "SELECT artist_id FROM artist WHERE name = '" + image_artist + "'"
    cursor.execute(query)
    response = cursor.fetchone()
    if ( response != None ):
        artist_id = int(response[0])
        query = "SELECT * FROM image WHERE artist_id = '" + str(artist_id) + "'"
        cursor.execute(query)
        response = cursor.fetchall()
        image_ids = []
        if ( response[0] == None ):
            print("<p> \nNo Results Found\n </p>")
        else:
            for row in response:
                image_ids.append(row[0])
            output = format.format_image_search(image_ids)
            print(output)
    else:
        print("<p> \nNo Results Found\n </p>")
    database.close()
    print("""
            </body>
          """)
    return 0

if __name__ == '__main__':
    main()
