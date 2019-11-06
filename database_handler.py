import cgi
import pymysql

class gallery:
    def __init__(self, id, name, des):
        self.id = int(id)
        self.name = str(name)
        self.des = str(des)

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name
    def get_description(self):
        return self.description

class image:
    def __init__(self, id, name, link, artist, gallery ):
        self.id = id
        self.name = name
        self.link = link
        self.artist = artist
        self.gallery = gallery

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_link(self):
        return self.link

    def get_gallery(self):
        return self.gallery

def initialize():
    database = pymysql.connect( host = 'localhost',
                                user = 'gallery',
                                passwd = 'eecs118',
                                database = 'gallery')
    if ( database != None ):
        print("Successfully linked database")
        return database
    else:
        print("An error occured. Exiting...")
        return -1

def closedatabase( database ):
    database.close()

def get_gallery_by_name( name ):
    database = initialize()
    if ( database == -1 ):
        print("database_handler.py: Error Linking the Database")

    cursor = database.cursor()
    query = "Select * FROM gallery WHERE name = %s" % name
    cursor.execute(query)

    if ( cursor == None ):
        print("database_handler.py: No database with name %s found" % name)
        return -1

    else:
        response = cursor.fetchone()
        gal = gallery(response[0], response[1], response[2])
        return gal

def get_gallery_by_id(id):
    database = initialize()
    if ( database == -1 ):
        print("database_handler.py: Error Linking the Database")

    cursor = database.cursor()
    query = "SELECT '" + id + "' FROM gallery"
    cursor.execute(query)

    if ( cursor == None ):
        print("database_handler.py: No database with id %d found" % id)
        return -1
    else:
        response = cursor.fetchone()
        gal = gallery(response[0], response[1], response[2])
        return gal

def get_all_images_in_gallery( name ):
    gal = get_gallery_by_name ( name )
    if ( gal == -1 ):
        print("database_handler.py get_all_images_in_gallery: Error. No database with name %s found" % name )
        return -1
    else:
        images = []
        query = "SELECT * FROM image WHERE gallery_id = %d" % gal.get_id()
        cursor.execute(query)
        for row in range(cursor.fetchall()):
            curr_image = image(row[0], row[1], row[2], row[3], row[4])
            images.append(curr_image)

        return images


def get_all_galleries():
    database = initialize()
    if ( database == -1 ):
        print("An error occured. Exiting")
        return -1

    cursor = database.cursor()
    sql = "SELECT * FROM gallery"
    cursor.execute(sql)
    all_galleries = []
    if ( cursor == None ):
        return -1
    else:
        for row in cursor.fetchall():
            current_entry = gallery(row[0], row[1], row[2])
            all_galleries.append(current_entry)
    closedatabase(database)
    return all_galleries
