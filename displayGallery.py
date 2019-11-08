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
    def set_detail(self, detail):
        self.detail = detail

class Gallery:
    def __init__(self, name, id, description):
        self.name = name
        self.id = id
        self.description = description
        self.images = []

    def get_id(self):
        return self.id
    def get_name(self):
        return self.name
    def get_description(self):
        return self.description
    def return_all_images(self):
        return self.images
    def add_image(self, image):
        self.images.append(image)

gallery = None

def request_artist_name(imageName):
    global gallery
    images = gallery.return_all_images()
    for image in images:
        if ( image.get_title() == imageName ):
            database = database_handler.initialize()
            if (database == -1 ):
                print("displayGallery.py request_artist_name(): Error Linking Database.\n")
            cursor = database.cursor()
            query = "SELECT name FROM artist WHERE artist_id = '" + str(image.get_artist_id()) + "'"
            cursor.execute(query)
            response = cursor.fetchone()
            artistName = response[0]
            return artistName
    #Artist Not Found
    return None

def request_gallery_name(imageName):
    global gallery
    images = gallery.return_all_images()
    for image in images:
        if (image.get_title() == imageName ):
             return gallery.get_name()
    return None

def request_image_data(imageName):
    global gallery
    images = gallery.return_all_images()
    for image in images:
        if (image.get_title() == imageName ):
             return image
    return None

def get_information(galleryName):
    global gallery
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

    query = "SELECT * FROM image WHERE gallery_id = '" + str(gallery.get_id()) + "'"
    cursor.execute(query)
    result = cursor.fetchall()
    for row in result:
        current_image = Image(row[0], row[1], row[2], row[3], row[4], row[5] )
        query = "SELECT * FROM detail WHERE image_id = " + str(current_image.image_id)
        cursor.execute(query)
        response = cursor.fetchone()
        if ( response == None ):
            continue
        detail = Detail(response[0], response[1], response[2], response[3], response[4], response[5], response[6], response[7])
        current_image.set_detail(detail)
        gallery.add_image(current_image)

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

    global gallery
    galleryName = ''
    output = ''
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
          """ % (galleryName.upper()))
    get_information(galleryName)
    num_of_images = len(gallery.return_all_images())

    output = output + """<h3> %s </h3>""" % gallery.get_description().upper()
    output = output + """<h3> Images in Gallery: """ + str(num_of_images) + """ </h3> </br>"""
    output = output + """<button type = 'button' onclick = 'viewImage()'> View Image </button></br>
                            <div id = 'viewImage'> </div>"""

    for image in gallery.return_all_images():
        output = output + """<div class = 'row text-center align-items-left'>
                            <div class = 'col-12 col-lg-6'> """
        output = output + """
                <h3> Title: %s </h3> </br>
                <h5> Link: %s  </h5> </br>
                """ % (image.get_title().capitalize(), image.get_link())
        output = output + """<div class = 'col-12 col-lg-6'>
                            <img class = 'image' src = %s alt = 'No Image Found >'""" % image.get_link()
        output = output + "</div></div>"
    print(output)
    print("""
            </body>
            <script>
                let viewImageInputBox = 0;
                function viewImage() {
                    if ( viewImageInputBox == 0 ){
                        document.getElementById('viewImage').innerHTML = `
                            <form action = '/test/cgi-bin/GalleryApp/displayImage.py'
                                method = 'POST' target = '__new'>
                                <label> Title </label> <input type = 'text' name = 'image_name' > </br>
                                <input type = 'submit' name = 'submit_image_view' value = 'View' />
                            </form>
                        `
                        viewImageInputBox = 1;
                    }
                    else {
                        document.getElementById('viewImage').innerHTML = ``
                        viewImageInputBox = 0;
                    }
                }
            </script>
        </html>
          """)
    return 0

if __name__ == '__main__':
    main()
