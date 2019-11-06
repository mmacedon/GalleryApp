#modify_artist.py

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

    artist_name = ''
    artist_new_name = ''
    artist_birth_year = ''
    artist_country = ''
    artist_description = ''

    form = cgi.FieldStorage()

    if ( form.getvalue ('artistName') ):
        artist_name = form.getvalue('artistName')
        artist_name = artist_name.lower()
    if ( form.getvalue('artistNewName') ):
        artist_new_name = form.getvalue('artistNewName')
        artsit_new_name = artist_new_name.lower()
    if ( form.getvalue('artistBirthYear') ):
        artist_birth_year = form.getvalue('artistBirthYear')
        artist_birth_year = artist_birth_year.lower()
    if ( form.getvalue('artistCountry') ):
        artist_country = form.getvalue('artistCountry')
        artist_country = artist_country.lower()
    if ( form.getvalue('artistDescription') ):
        artist_description = form.getvalue('artistDescription')
        artist_description = artist_description.lower()

    if ( artist_name == '' or artist_new_name == '' ):
        print("""
            <body>
                <h1>modify_artist.py: main(): Need to input artist name fields. </h1>
            </body>
            """)
        print(form)
    else:
        database = database_handler.initialize()
        if ( database == -1 ):
            print("modify_artist.py: main(): There was an error retrieving the database.")

        cursor = database.cursor()

        query = "SELECT artist_id FROM artist WHERE name = '" + artist_name + "'"
        cursor.execute(query)
        response = cursor.fetchone()

        query = "SELECT artist_id FROM artist WHERE name = '" + artist_new_name + "'"
        cursor.execute(query)
        response_2 = cursor.fetchone()

        if ( response == None ):
            print("modify_artist.py: main(): The Artist Does not Exist!")
        else:
            artist_id = int( response[0] )
            second_artist_id = int(response_2[0])
            if ( artist_id == second_artist_id ):
                query = 'UPDATE artist SET name = %s, birth_year = %s, country = %s, description = %s WHERE artist_id = %s'
                values = (artist_new_name, artist_birth_year, artist_country, artist_description, artist_id )
                cursor.execute(query, values)
                database.commit()
            else:
                print("There is already another artist with name %s" % artist_new_name)

        database.close()
        print("""
            <script>window.close()</script>
            """)
    return 0

if __name__ == '__main__':
    main()
