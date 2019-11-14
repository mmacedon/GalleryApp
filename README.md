Manuel Macedonio
EECS 118 Knowledge Engineering and Software Engineering
Mini Project 3:
# GalleryApp
 Web application used to store and view images.

The web application allows users to create a gallery to organize and store images
using image links. The user can input information about the image such as a
description, tile, and the artist.
The user can further input the details of the image such as the location of
the image, the year it was created, the size, and the type of image it is.
The user can also modify the details of the artist such as their birth year or
the country the reside.
The user can create new galleries, images and artists. The user can also delete
images and galleries if they wish to do so.
The GalleryApp also allows users to search for images based on the gallery,
artist, type, year or location. The user can also search for an artist based
on their country or birth year.

Initialization:
  Prior to using the galleryApp, you must have Apache TomCat server running.
  The galleryApp calls its modules through the following directory.
    "/test/cgi-bin/GalleryApp/."
  Ensure that the galleryApp is placed inside the proper directory to ensure that
  there are no errors when calling the python modules.

Usage and Notes:
  The GalleryApp is used through text based input. Mouse clicks are used when opening
  menus that allow users to input information.
  Galleries are required for images. You must input a gallery that already exists
  when creating a new image.
  An existing artist is not necessary. If an image is inputted with an artist
  name that does not exist, then the GalleryApp will input the name of the artist
  into the database with 'NoData' for its columns and 0 for any integer values.
  The user can modify these details later.
  Modules that create new instances and modify instances run their modules and close
  whether or not inputting the data is successful. If it is not successful, Check
  to see if the information was inputted correctly. If the instance does appear
  when the result is searched for, then it was successful.

The entire GalleryApp can be found on GitHub:
  https://github.com/mmacedon/GalleryApp
