#search_image_location.py

import cgi
import database_handler
import pymysql
import format

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

    image_location = ''

    form = cgi.FieldStorage()

    if ( form.getvalue('location_name') ):
        image_location = form.getvalue('location_name')
        image_location = image_location.lower()

    if ( image_location == '' ):
        print("<body> search_image_location.py main(): Error! Need to input field.")
        print("</body>")
        return 0

    print("""
        <body>
            <h1> Image Results with Location %s </h1>
        """ % image_location)

    database = database_handler.initialize()
    if ( database == -1 ):
        print("search_image_type.py main(): Error linking database.")
        return 0
    cursor = database.cursor()
    query = "SELECT image_id FROM detail WHERE location = '" + image_location + "'"
    cursor.execute(query)
    response = cursor.fetchall()
    image_ids = []
    if ( response == None ):
        print("<p> \nNo Results Found\n </p>")
    else:
        for row in response:
            image_ids.append(row[0])
        output = format.format_image_search(image_ids)
        print(output)
    print("""
            </body>
          """)
    return 0

if __name__ == '__main__':
    main()
