#modify_detail.py

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

    detailTitle = ''
    detailYear = 0
    detailType = ''
    detailWidth = 0
    detailHeight = 0
    detailLocation = ''
    detailDescription = ''

    form = cgi.FieldStorage()

    if ( form.getvalue('detailTitle') ):
         detailTitle = form.getvalue('detailTitle')
         detailTitle = detailTitle.lower()
    if ( form.getvalue('detailYear') ):
         detailYear = form.getvalue('detailYear')
    if ( form.getvalue('detailType') ):
         detailType = form.getvalue('detailType')
         detailType = detailType.lower()
    if ( form.getvalue('detailWidth') ):
         detailWidth = form.getvalue('detailWidth')
    if ( form.getvalue('detailHeight') ):
         detailHeight = form.getvalue('detailHeight')
    if ( form.getvalue('detailLocation') ):
         detailLocation = form.getvalue('detailLocation')
         detailLocation = detailLocation.lower()
    if ( form.getvalue('detailDescription') ):
         detailDescription = form.getvalue('detailDescription')
         detailDescription = detailDescription.lower()

    if ( detailTitle == '' ):
        print("new_detail.py main(): Error. Input Name Field")
        return 0
    else:
        database = database_handler.initialize()
        if ( database == -1 ):
            print("new_detail.py main(): There was an error retrieving the database.")

        cursor = database.cursor()

        #Find the image that corresponds to the details:
        query = "SELECT image_id FROM image WHERE title = '" + detailTitle + "'"
        cursor.execute(query)
        response = cursor.fetchone()

        if ( response == None ):
            print("modify_detail.py main(): Error! No image with name %s found." % detailTitle)
        else:
            image_id = int(response[0])

            query = "SELECT detail_id FROM detail WHERE image_id = '" + str(image_id) + "'"
            cursor.execute(query)

            response = cursor.fetchone()
            if ( response == None ):
                print("modify_detail.py main(): Error! Something went wrong")
            else:
                detail_id = int(response[0])
                query = 'UPDATE detail SET year = %s, type = %s, width = %s, height = %s, location = %s, description = %s WHERE detail_id = %s'
                values = (detailYear, detailType, detailWidth, detailHeight, detailLocation, detailDescription, detail_id )
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
