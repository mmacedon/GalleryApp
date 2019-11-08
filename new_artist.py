#new_artist.py

import database_handler
import cgi

def insert_new_artist( artist_name ):
    database = database_handler.initialize()
    if ( database == -1 ):
        print("Error Linking Database")
    else:
        print("new_artist.py insert_new_artist: Successfully linked database")
    cursor = database.cursor()

    #Check if the artist already exists:
    query = "SELECT artist_id from artist WHERE name = '" + artist_name + "'"
    cursor.execute(query)
    response = cursor.fetchone()
    if ( response != None ):
        print("new_artist.py: insert_new_artist: Artist already exists")
        artist_id = int(response[0])
    else:
        #Get the New artist ID:
        query = "SELECT MAX(artist_id) from artist"
        cursor.execute(query)
        response = cursor.fetchone()
        if ( response[0] == None ):
            print("new_artist.py: insert_new_artist: No Artist in the Table")
            artist_id = 0
        else:
            artist_id = int(response[0]) + 1
        query = "INSERT IGNORE INTO artist(artist_id, name, birth_year, country, description) VALUES(%s, %s, %s, %s, %s)"
        values = (artist_id, artist_name, 0, 'No Data', 'No Data')
        cursor.execute(query, values)
        database.commit()
    database.close()
    return artist_id

def main():
    artist_id = ''
    artist_name = ''
    artist_birth_year = 0
    artist_country = ''
    artist_description = ''

    form = cgi.FieldStorage()
    if ( form.getvalue('artist_name') ):
        artist_name = form.getvalue('artist_name')
        artist_name = artist_name.lower()
    if ( form.getvalue('artist_birth_year')):
        artist_birth_year = form.getvalue('artist_birth_year')
    if ( form.getvalue('artist_country')):
        artist_country = form.getvalue('artist_country')
        artist_country = artist_country.lower()
    if ( form.getvalue('artist_description')):
        artist_description = form.getvalue('artist_description')
        artist_description = artist_description.lower()

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
    </head>""")

    if ( artist_name == '' ):
        print("Error. Need to input name field")

    ##Check if the artist already exists
    if ( artist_country == '' ):
        artist_country = 'No Data'
    if ( artist_description == '' ):
        artist_description = 'No Data'
        
    database = database_handler.initialize()
    if ( database == -1 ):
        print("new_artist.py add_artist: Error Linking Database")
    else:
        print("new_artist.py add_artist: Successfully linked database")
    cursor = database.cursor()

    query = "SELECT artist_id FROM artist WHERE name = '" + artist_name + "'"
    cursor.execute(query)
    response = cursor.fetchone()
    if ( response != None ):
        print("The artist already exists")
    else:
        query = "SELECT MAX(artist_id) FROM artist"
        cursor.execute(query)
        response = cursor.fetchone()
        if ( response == None ):
            artist_id = 0
        else:
            artist_id = int(response[0]) + 1

        query = "INSERT IGNORE INTO artist(artist_id, name, birth_year, country, description) VALUES(%s, %s, %s, %s, %s)"
        values = (artist_id, artist_name, artist_birth_year, artist_country, artist_description)
        cursor.execute(query, values)
        database.commit()
    database.close()
    print( """
        <script>
            window.close()
        </script>
    """)

if __name__ == '__main__':
    main()
