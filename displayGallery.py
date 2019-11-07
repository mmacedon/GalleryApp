#displayGallery.py

import cgi
import database_handler
import pymysql

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

class Gallery:
    def __init__(self, name, id, description):
        self.name = name
        self.id = id
        self.description = description
        self.images = []
        self.imagelinks = []

    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def get_description(self):
        return self.description
    def return_all_images(self):
        return self.images
    def return_all_image_links(self):
        return self.imagelinks


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

    galleryName = ''

    form = cgi.FieldStorage()
    if ( form.getvalue('gallery_name') ):
        galleryName = form.getvalue('gallery_name')
        galleryName = galleryName.lower()

    if ( galleryName == '' ):
        print("displayGallery.py main(): Error! Need to input the Gallery Name\n")
        return 0

    print("""
        <body>
            <h1> Displaying Images in %s Gallery </h1>
          """ % galleryName )

    database = database_handler.initialize()
    if ( database == -1 ):
        print("displayGallery.py main(): Error Linking Database\n")
        return 0
    cursor = database.cursor()

    query = "SELECT * FROM gallery WHERE name = '" + galleryName + "'"
    cursor.execute(query)
    result = cursor.fetchone()

    if ( result == None ):
        print("Error! No Gallery with Name %s.\n" % galleryName.capitalize())
        return 0

    gallery = Gallery(result[1], result[0], result[2])

    query = "SELECT * FROM image WHERE gallery_id = '" + str(gallery.get_id())
    cursor.execute(query)
    result = cursor.fetchall()

    for row in response:
        current_image = Image(row[0],
        ##########################)
    return 0

if __name__ == '__main__':
    main()
