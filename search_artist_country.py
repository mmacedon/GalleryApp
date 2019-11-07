#search_artist_country.py
import database_handler
import cgi
import pymysql
import format

class Image:
    def __init__(self, image_id, title, link, gallery_id, artist_id, detail_id):
        self.image_id = image_id
        self.title = title
        self.link = link
        self.gallery_id = gallery_id
        self.artist_id = artist_id
        self.detail_id = detail_id

    def get_image_id(self):
        return self.image_id
    def get_title(self):
        return self.title
    def get_link(self):
        return self.link
    def get_gallery_id(self):
        return self.gallery_id
    def get_artist_id(self):
        return self.artist_id
    def get_detail_id(self):
        return self.detail_id

class Artist:
    def __init__(self, id, name, birth_year, country, description):
        self.id = id
        self.name = name
        self.birth_year = birth_year
        self.country = country
        self.description = description
        self.images = []

    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def get_birth_year(self):
        return self.birth_year
    def get_country(self):
        return self.country
    def get_description(self):
        return self.description

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

    artist_country = ''

    form = cgi.FieldStorage()

    if ( form.getvalue('artist_country') ):
        artist_country = form.getvalue('artist_country')
        artist_country = artist_country.lower()

    if ( artist_country == '' ):
        print("search_artist_country.py main(): Error! Need to input Country Field")
        return 0
    print("""
        <body>
            <h1> Results for Artists from Country %s </h1>
    """ % artist_country )

    database = database_handler.initialize()

    if ( database == -1 ):
        print("search_artist_country.py main(): Error linking database.")
        return 0
    cursor = database.cursor()

    query = "SELECT * FROM artist WHERE country = '" + artist_country + "'"
    cursor.execute(query)
    response = cursor.fetchall()
    artists = []
    if ( response == None ):
        print("No Artists Found From Country %s" % artist_country)
        return 0

    for row in response:
        current_artist = Artist(response[0][0], response[0][1], response[0][2], response[0][3], response[0][4])
        artists.append(current_artist)

    for artist in artists:
        query = "SELECT * FROM image WHERE artist_id = '" + str(artist.get_id()) + "'"
        cursor.execute(query)
        response = cursor.fetchall()
        if ( response == None ):
            continue
        else:
            for row in response:
                current_image = Image(response[0][0], response[0][1], response[0][2], response[0][3], response[0][4], response[0][5])
                print(current_image)
                artist.images.append(current_image)

    output = format.format_artist_search(artists)
    print(output)
    print("""
        </body>
    """)

    return 0

if __name__ == '__main__':
    main()
