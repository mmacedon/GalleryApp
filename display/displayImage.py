#displayImage.py
import cgi
import database_handler
import pymysql

class Artist:
    def __init__(self, artist_id, name, birth_year, country, description ):
        self.artist_id = artist_id
        self.name = name
        self.birth_year = birth_year
        self.country = country
        self.description = description

    def get_artist_id(self):
        return self.artist_id
    def get_name(self):
        return self.name
    def get_birth_year(self):
        return self.birth_year
    def get_country(self):
        return self.country
    def get_description(self):
        return self.description

class Detail:
    def __init__(self, detail_id, image_id, year, type, width, height, location, description):
        self.detail_id = detail_id
        self.image_id = image_id
        self.year = year
        self.type = type
        self.width = width
        self.height = height
        self.location = location
        self.description = description

    def get_detail_id(self):
        return self.detail_id
    def get_image_id(self):
        return self.image_id
    def get_year(self):
        return self.year
    def get_type(self):
        return self.type
    def get_width(self):
        return self.width
    def get_height(self):
        return self.height
    def get_location(self):
        return self.location
    def get_description(self):
        return self.description

class Image:
    def __init__(self, image_id, title, link, gallery_id, artist_id, detail_id):
        self.image_id = image_id
        self.title = title
        self.link = link
        self.gallery_id = gallery_id
        self.artist_id = artist_id
        self.detail_id = detail_id
        self.detail = None

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
    def get_detail(self):
        return self.detail
    def set_detail(self, detail):
        self.detail = detail

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

    imageName = ''
    output = ''
    form = cgi.FieldStorage()
    if ( form.getvalue('image_name') ):
        imageName = form.getvalue('image_name')
        imageName = imageName.lower()

    if ( imageName == '' ):
        print("<h1> Error! Need to Input an Image Name!")
        return -1

    database = database_handler.initialize()
    if ( database == -1 ):
        print("Error linking database")
        return 0
    cursor = database.cursor()

    query = "SELECT * FROM image WHERE title = '" + imageName + "'"
    cursor.execute(query)
    response = cursor.fetchone()
    if ( response == None ):
        print("Error: Image not Found")
        return -1

    image = Image(response[0], response[1], response[2], response[3], response[4], response[5])
    query = "SELECT * FROM detail WHERE image_id = '" + str(image.get_image_id()) + "'"
    cursor.execute(query)
    response = cursor.fetchone()
    detail = Detail(response[0], response[1], response[2], response[3], response[4], response[5], response[6], response[7])
    image.set_detail(detail)

    query = "SELECT name FROM gallery WHERE gallery_id = '" + str(image.get_gallery_id()) + "'"
    cursor.execute(query)
    response = cursor.fetchone()
    galleryName = response[0]

    query = "SELECT * FROM artist WHERE artist_id = '" + str(image.get_artist_id()) + "'"
    cursor.execute(query)
    response = cursor.fetchone()
    artist = Artist(response[0], response[1], response[2], response[3], response[4])

    output = output + """
                        <h1> %s </h1> </br>
                        <img class = 'image' src = %s alt = 'No Image Found'> </br>
                        <h3> Description: %s </h3> </br>
                        <h3> Gallery: %s     </h3> </br>
                        <h3> Artist: %s      </h3>
                        <button type = 'button' onclick ='displayArtistDetails()'> Show Artist Details </button> </br>
                        <div id = 'artistDetails'></div>
                        <h4> Details:        </h4> </br>
                        <h6> Year: %s        </h6> </br>
                        <h6> Type: %s        </h6> </br>
                        <h6> Width: %s       </h6> </br>
                        <h6> Height: %s      </h6> </br>
                        <h6> Location: %s    </h6> </br>
                        """ % (image.get_title().upper(), image.get_link(), image.get_detail().get_description().capitalize(),
                                galleryName.upper(), artist.get_name().upper(), image.get_detail().get_year(), image.get_detail().get_type().upper(),
                                image.get_detail().get_width(), image.get_detail().get_height(), image.get_detail().get_location().upper() )
    print("""<script>
            let displayingArtist = 0;
            function displayArtistDetails () {
                if (displayingArtist == 0 ){
                    document.getElementById('artistDetails').innerHTML = `
                        <h6> Birth Year: %s </h6>
                        <h6> Country: %s </h6>
                        <h6> Description: %s </h6>
                    `
                    displayingArtist = 1;
                }
                else {
                    document.getElementById('artistDetails').innerHTML = ``
                    displayingArtist = 0;
                }
            }
    </script>""" % (artist.get_birth_year(), artist.get_country(), artist.get_description()))
    print(output)
    return 0

if __name__ == '__main__':
    main()
