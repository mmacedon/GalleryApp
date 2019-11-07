#search_image_year.py

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
        </head>""")

    start_year = 0
    end_year = 10e8

    form = cgi.FieldStorage()

    if ( form.getvalue('start_year') ):
        start_year = int(form.getvalue('start_year'))
    if ( form.getvalue('end_year') ):
        end_year   = int(form.getvalue('end_year'))

    if ( start_year == 0 and end_year == 10e8 ):
        print("""<body>
                    <h1> Error! Need to input at least one of the years <h1>
                 </body>
              """)
        return 0
    else:
        print("""
            <body>
                <h1> Image Results for Given Range: %s - %s </h1>
            """ % (str(start_year), str(end_year)))

        image_ids = []
        database = database_handler.initialize()
        if ( database == -1 ):
            print("search_image_year.py main(): Error linking database")
            return 0
        cursor = database.cursor()

        query = "SELECT image_id FROM detail WHERE year >'" + str(start_year) + "' and year < '" + str(end_year) + "'"
        cursor.execute(query)
        response = cursor.fetchall()
        if ( response == None ):
            print("<p>\nNo Results found.\n</p>")
            return 0
        else:
            for row in response:
                image_ids.append(row[0])
            output = format.format_image_search(image_ids)
        database.close()
        print(output)
        print("""
                </body>
              """)
        return 0
    return 0

if __name__ == '__main__':
    main()
