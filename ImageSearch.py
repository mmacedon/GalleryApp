import cgi
import pymysql

class SearchQuery:
    def __init__ ( self, type, start_year, end_year, artist, location ):
        self.type = type
        self.start_year = start_year
        self.end_year = end_year
        self.artist = artist
        self.location = location

form = cgi.FieldStorage()

type = form.getvalue('type') if form.getvalue('type') else None
start_year = form.getvalue('start_year') if form.getvalue('start_year') else None
end_year = form.getvalue('end_year') if form.getvalue('start_year') else None
artist = form.getvalue('artist') if form.getvalue('artist') else None
location = form.getvalue('location') if form.getvalue('location') else None

query = SearchQuery(type, start_year, end_year, artist, location)
