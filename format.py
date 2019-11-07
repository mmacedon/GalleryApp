#format.py
import database_handler
import cgi

class Gallery:
    def __init__(self, name, id, description):
        self.name = name
        self.id = id
        self.description = description
        self.images = []
        self.imagelinks = []

    def return_all_images(self):
        return images

def format_image_search( ids ):
    output = ''
    title = []
    images = []
    descriptions = []
    types = []
    years = []
    widths = []
    heights = []
    locations = []
    artist_ids = []
    artists = []
    database = database_handler.initialize()
    if ( database == -1 ):
        print("format.py format_image_search(): Error linking database.")
        return 0
    cursor = database.cursor()
    for id in ids:
        query = "SELECT * FROM image WHERE image_id = '" + str(id) + "'"
        cursor.execute(query)
        response = cursor.fetchall()
        title.append(response[0][1])
        images.append(response[0][2])
        artist_ids.append(response[0][4])

    for id in ids:
        query = "SELECT * FROM detail WHERE image_id = '" + str(id) + "'"
        cursor.execute(query)
        response = cursor.fetchall()
        years.append(response[0][2])
        types.append(response[0][3])
        widths.append(response[0][4])
        heights.append(response[0][5])
        locations.append(response[0][6])
        descriptions.append(response[0][7])

    for id in artist_ids:
        query = "SELECT name FROM artist WHERE artist_id = '" + str(id) + "'"
        cursor.execute(query)
        response = cursor.fetchall()
        artists.append(response[0][0])

    output = """<div class = 'row text-center'>
                    <div class = 'col-12 col-lg-6 col-md-4 search_layout'>
             """
    for i in range(len(title)):
        output = output + """
                    <h3> %s </h3>
                    <img class = 'image' src = %s alt = 'No Image Found'>
                    <h5> %s </h5>
                    """ % (title[i].capitalize(), images[i], descriptions[i].capitalize())
        output = output + """
                        <h4> Details </h4></br>
                        <h6> Year: %s </h6>
                        <h6> Artist: %s </h6>
                        <h6> Type: %s </h6>
                        <h6> Location: %s </h6>
                        """ % (years[i], artists[i], types[i], locations[i])
    output = output + """</div>
                    </div>"""

    return output

def format_galleries ( all_galleries ):

    formatted_galleries = []
    database = database_handler.initialize()
    if ( database == -1 ):
        print("format.py format_galleries(): Error linking database\n")
        return 0
    cursor = database.cursor()

    for gallery in all_galleries:
        print (gallery)
        input = Gallery(gallery.name, gallery.id, gallery.description)
        current_id = int(input.id)
        query = "SELECT link FROM image WHERE gallery_id = '" + str(current_id) + "'"
        cursor.execute(query)
        for row in cursor.fetchall():
            input.imagelinks.append(row[0])
        formatted_galleries.append(input)

    database.close()
    output = """
        <div class = 'row text-center'>
            <div class = 'col-12 col-lg-6 col-md-4 gallery_layout'>"""

    for gallery in formatted_galleries:
        output = output + """<h2> """ + gallery.name.capitalize() + """</h2></br> """
        output = output + """<h6> """ + gallery.description.capitalize() + """</h6></br>"""
        if ( len(gallery.imagelinks) == 0 ):
            continue
        else:
            output = output + """
                <img class = 'image' src = """ + gallery.imagelinks[0] + """ alt = 'No Image Found'> </br>
            """
    output = output + """
            </div>
        </div>
    """
    return output
