#displayImage.py
import cgi
import database_handler
from displayGallery import request_image_data, request_artist_name, request_gallery_name
import pymysql

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

    #image = displayGallery.request_image_data(imageName)
    #detail = displayGallery.request_datail_data(imageName)
    #galleryName = displayGallery.request_gallery_name(imageName)
    #artistName = displayGallery.request_artist_name(imageName)
    image = request_image_data(imageName)
    galleryName = request_gallery_name(imageName)
    artistName = request_artist_name(imageName)

    if ( image == None ):
        print("<h1> Error! Image \'%s\' not found." % imageName)
        return -1
    output = output + """
                        <h1> %s </h1> </br>
                        <img class = 'image' src = %s alt = 'No Image Found'> </br>
                        <h3> Description: %s </h3> </br>
                        <h3> Gallery: %s     </h3> </br>
                        <h3> Artist: %s      </h3>
                        <form action = '/test/cgi-bin/GalleryApp/view_artist.py'
                            method = 'POST' target = '__new'>
                            <input type = 'submit' name = 'view_artist' value = 'View Artist' /> </br>
                        </form>
                        <h4> Details:        </h4> </br>
                        <h6> Year: %s        </h6> </br>
                        <h6> Type: %s        </h6> </br>
                        <h6> Width: %s       </h6> </br>
                        <h6> Height: %s      </h6> </br>
                        <h6> Location: %s    </h6> </br>
                        """ % (image.get_title(), image.get_link(), image.get_detail().get_description(),
                                galleryName, artistName, image.get_detail().get_year(), image.get_detail().get_type(),
                                image.get_detail().get_width(), image.get_detail().get_height(), image.get_detail().get_location() )
    print(output)
    return 0

if __name__ == '__main__':
    main()
