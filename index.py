import cgi
import pymysql
import datetime
import database_handler

database = database_handler.initialize()
cursor = database.cursor()

if ( cursor == -1 ):
    print("Something went wrong with the database\n")
    exit()

current_time = datetime.datetime.now()

current_hour = current_time.hour
greeting_message = "Hello, good "
if ( current_hour < 12 ):
    greeting_message = greeting_message + "morning"
elif ( current_hour > 12 and current_hour < 18 ):
    greeting_message = greeting_message + "afternoon"
else:
    greeting_message = greeting_message + "evening"
greeting_message = greeting_message + ". It is a pleasure to see you."

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

        <body>

            <header>
                <div class = "container">
                    <div class = "row">
                        <div class = "col text-center">
                            <h1> PhotoGala </h1>
                            <p> Your personal photo gallery </p>
                            <p> """ + greeting_message + """
                        </div>
                    </div>
                </div>
            </header>

            <div class="section section-1 options">
                <div class = "container">
                    <div class = "row justify-content-around align-items-center">
                        <div class = "col-5">
                            <h3 class = "col-12"> List </h3>
                            <button type = "button" onclick = 'List_All_Galleries()'>All Galleries </button> </br>
                        </div>
                        <div class = "col-5">
                            <h3 class = "col-10"> Create </h3>
                            <button type = "button" onclick = 'Create_New_Gallery()'>New Gallery </button> </br>
                            <div id = "input_gallery"></div>
                            <button type = "button" onclick = 'Create_New_Artist()'>New Artist </button> </br>
                            <div id = "input_artist"></div>
                            <button type = "button" onclick = 'Create_New_Image()'>New Image </button> </br>
                            <div id = "input_image"></div>
                        </div>
                        <div class = "col-2">
                            <h3> Modify </h3>
                            <button type = "button" onclick = 'Modify_Gallery()'>Gallery </button> </br>
                            <div id = "modifyGallery"></div>
                            <button type = "button" onclick = 'Modify_Artist()'>Artist </button> </br>
                            <div id = "modifyArtist"></div>
                            <button type = "button" onclick = 'Modify_Image()'>Image </button></br>
                            <div id = "modifyImage"></div>
                            <button type = "button" onclick = 'Modify_Detail()'>Image Details </button></br>
                            <div id = "modifyDetail"></div>
                        </div>
                    </div>
                </div>
            </div>
            </br>

            <div class = "section section-2 search-options">
                <div class = "container">
                    <div class = "row">
                        <h2> Search </h2>
                    </div>
                    <div class = "row justify-contents-around">
                        <h4>Images:</h4>
                            <form action = '/test/cgi-bin/GalleryApp/ImageSearch.py'
                                    method = 'POST' target = '__new'>

                                <div class = "col-12 col-lg-6">
                                        <label>Type:</label>
                                        <input type = "text" name = "image_type"></br>
                                        <label>Year:</label>
                                        <input type = "text" name = "start_year"> -
                                        <input type = "text" name = "end_year">
                                </div>
                                <div class = "col-12 col-lg-6">
                                        <label>Artist:</label>
                                        <input type = "text" name = "artist_name"></br>
                                        <label>Location:</label>
                                        <input type = "text" name = "location_name"></br>
                                </br>
                                </div>
                                <input type = 'submit' name = 'submit_image_search' value = 'Submit' />
                            </form>
                    </div>

                    <div class ="row justify-contents-around">
                        <h4>Artist:</h4>
                            <form action = '/test/cgi-bin/GalleryApp/ArtistSearch.py'
                                    method = 'POST' target = '_new'>
                                <div class = "col-12 col-lg-6">
                                    <label>Country:</label>
                                    <input type = "text" name = "artist_country">
                                </div>
                                <div class = "col-12 col-lg-6">
                                    <label>Birth Year:</label>
                                    <input type = "text" name = "artist_birth_year"></br>
                                </div>
                                <input type = 'submit' name = 'submit_artist_search' value = 'Submit' />
                            </form>
                    </div>
                </div>
                </br>
                <div class = "section section-3 delete-options">
                    <div class = "container">
                        <div class = "row text-center justify-content-around align-items-center">
                            <h2> Delete </h2>
                                <form action = "/test/cgi-bin/GalleryApp/delete.py"
                                    method = 'POST' target = '__new'>
                                    <div class = "col-12">
                                    <label> Gallery </label> <input type = "text" name = "delete_gallery">
                                    <label> Image   </label> <input type = "text" name = "delete_image"  >
                                    <label> Artist  </label> <input type = "text" name = "delete_artist" >
                                    <input type = "submit" name = "submit_deletion" value = "Delete" />
                                </form>
                        </div>
                        <p> Warning: Deleting a gallery will delete all images in it as well.
                            Once deleted, it can be undone. Do so with caution. </p>
                    </div>
                </div>
                <div class = "section section-4 display">
                    <div class = "container">
                        <div class = "row text-center justify-content-around align-items-center">
                            <div class = "col-12 col-lg-6 gallerylist">
                                <h2> Gallery List </h2>
                                <p> Currently no Images to display </p>
                            </div>
                            <div class = "col-12 col-lg-6 imageview">
                                <h2> Image View </h2>
                                <p> No Image </p>
                            </div>
                        </div>
                    </div>
            </div>

            <script>

            function List_All_Galleries() {}

<!----- Create Images Function -------->
            let gallery_input_box = 0;
            let artist_input_box = 0;
            let image_input_box = 0;

            function Create_New_Image() {
                if (image_input_box == 0) {
                    document.getElementById('input_image').innerHTML = `
                        <form action = '/test/cgi-bin/GalleryApp/new_image.py'
                         method = 'POST' target = '__new'>
                            <label> Title    </label> <input type = 'text' name = 'name'    > </br>
                            <label> Link     </label> <input type = 'text' name = 'link'    > </br>
                            <label> Artist   </label> <input type = 'text' name = 'artist'  > </br>
                            <label> Gallery  </label> <input type = 'text' name = 'gallery' > </br>
                            <input type = 'submit' name = 'submit_new_image'  value = 'Submit' />
                        </form> `
                        image_input_box = 1;
                }
                else {
                    document.getElementById('input_image').innerHTML = ` `
                    image_input_box = 0;
                }
            }

            function Create_New_Artist() {
                if ( artist_input_box == 0 ) {
                    document.getElementById('input_artist').innerHTML = `
                    <form action = '/test/cgi-bin/GalleryApp/new_artist.py'
                    method = 'POST' target = '__new'>
                        <label>Name         </label><input type = 'text' name = 'artist_name'></br>
                        <label>Birth Year   </label><input type = 'text' name = 'artist_birth_year'></br>
                        <label>Country      </label><input type = 'text' name = 'artist_country'></br>
                        <label>Description  </label><input type = 'text' name = 'artist_description'>
                        <input type = 'submit' name = 'submit_new_artist'  value = 'Submit' />
                    </form> `
                    artist_input_box = 1;
                }
                else {
                    document.getElementById('input_artist').innerHTML = ``
                    artist_input_box = 0;
                }
            }

            function Create_New_Gallery() {
                if ( gallery_input_box == 0 ) {
                    document.getElementById('input_gallery').innerHTML = `
                        <form action = '/test/cgi-bin/GalleryApp/new_gallery.py'
                        method = 'POST' target = '__new'>
                            <label> Name        </label><input type = 'text' name = 'gal_name'></br>
                            <label> Description </label><input type = 'text' name = 'gal_description'></br>
                            <input type = 'submit' name = 'submit_new_gallery'  value = 'Submit' />
                        </form> `
                    gallery_input_box = 1;
                }
                else {
                    document.getElementById('input_gallery').innerHTML = ``
                    gallery_input_box = 0;
                }
            }

            let modifyGalleryInputBox = 0;
            let modifyArtistInputBox = 0;
            let modifyImageInputBox = 0;
            let modifyDetailInputBox = 0;
            function Modify_Gallery() {
                if ( modifyGalleryInputBox == 0 ) {
                    document.getElementById('modifyGallery').innerHTML = `
                        <form action = '/test/cgi-bin/GalleryApp/modify_gallery.py'
                            method = 'POST' target = '__new'
                            <label> Name            </label> <input type = 'text' name = 'galleryName'></br>
                            <label> New Name        </label> <input type = 'text' name = 'galleryNewName'></br>
                            <label> New Description </label> <input type = 'text' name = 'galleryDescription'></br>
                            <input type = 'submit' name = 'submitModifiedGallery' value = 'Submit' />
                        </form>
                        `
                    modifyGalleryInputBox = 1;
                }
                else {
                    document.getElementById('modifyGallery').innerHTML = ``
                    modifyGalleryInputBox = 0;
                }
            }

            function Modify_Artist() {
            if ( modifyArtistInputBox == 0 ) {
                document.getElementById('modifyArtist').innerHTML = `
                <form action = '/test/cgi-bin/GalleryApp/modify_artist.py'
                    method = 'POST' target = '__new'>
                    <label> Artist Name </label> <input type = 'text' name = 'artistName'></br>
                    <label> New Name    </label> <input type = 'text' name = 'artistNewName'></br>
                    <label> Birth Year  </label> <input type = 'text' name = 'artistBirthYear'></br>
                    <label> Country     </label> <input type = 'text' name = 'artistCountry'></br>
                    <label> Description </label> <input type = 'text' name = 'artistDescription'></br>
                    <input type = 'submit' name = 'submitModifiedArtist' value = 'Submit' />
                `
                modifyArtistInputBox = 1;
            }
            else {
                document.getElementById('modifyArtist').innerHTML = ``
                modifyArtistInputBox = 0;
                }
            }

            function Modify_Image() {
                if ( modifyImageInputBox == 0 ) {
                    document.getElementById('modifyImage').innerHTML = `
                        <form   action = '/test/cgi-bin/GalleryApp/modify_image.py'
                        method = 'POST' target = '__new'>
                            <label> Image Title </label> <input type = 'text' name = 'imageTitle'></br>
                            <label> New Title   </label> <input type = 'text' name = 'imageNewTitle'></br>
                            <label> Image Link  </label> <input type = 'text' name = 'imageLink'></br>
                            <label> Gallery     </label> <input type = 'text' name = 'imageGallery'></br>
                            <label> Artist      </label> <input type = 'text' name = 'imageArtist'></br>
                            <label> Detail      </label> <input type = 'text' name = 'imageDetail'></br>
                            <input type = 'submit' name = 'submitModifiedImage' value = 'Submit' />
                        </form>
                    `
                    modifyImageInputBox = 1;
                }
                else {
                    document.getElementById('modifyImage').innerHTML = ``
                    modifyImageInputBox = 0;
                }
            }

            function Modify_Detail() {
                if ( modifyDetailInputBox == 0 ) {
                    document.getElementById('modifyDetail').innerHTML = `
                    <form action = '/test/cgi-bin/GalleryApp/modify_detail.py'
                    method = 'POST' target = '__new'>
                        <label> Image Title </label> <input type = 'text' name = 'detailTitle'> </br>
                        <label> Year        </label> <input type = 'text' name = 'detailYear'> </br>
                        <label> Type        </label> <input type = 'text' name = 'detailType'> </br>
                        <label> Width       </label> <input type = 'text' name = 'detailWidth'> </br>
                        <label> Height      </label> <input type = 'text' name = 'detailHeight'> </br>
                        <label> Location    </label> <input type = 'text' name = 'detailLocation'> </br>
                        <label> Description </label> <input type = 'text' name = 'detailDescription'> </br>
                        <input type = 'submit' name = 'submitModifiedDetail' value = 'Submit' />
                    </form>
                    `
                    modifyDetailInputBox = 1;
                }
                else {
                    document.getElementById('modifyDetail').innerHTML = ``
                    modifyDetailInputBox = 0;
                }
            }
            </script>
        </body>
    """)
