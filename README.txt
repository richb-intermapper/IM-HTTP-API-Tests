InterMapper HTTP API Test Cases

This repository holds Python programs that test importing and exporting to/from 
InterMapper using its HTTP API.

These are quick and dirty programs, with relatively little error handling. They also
have a certain amount of system-dependencies that would have to be tweaked to get them
to run in other settings.

1) importer2.py

This program retrieves images from several places, then imports them into InterMapper
for use as map backgrounds and icons. It gets icons from:

- Desktop Earth images, that show the world, with the daylight/nighttime terminator
	accurately displayed. http://www.codefromthe70s.org/desktopearth.aspx
	
- Current Weather map from Weather.com

- An icon that displays the current HH:MM created with ImageMagick

The program regularly retrieves/creates these images, then imports them into 
InterMapper using the HTTP API.

2) mapreaper.py

This program retrieves a background image from a specified map on a regular basis and
saves it to a folder. If you point it at the map that's getting the Desktop Earth images
retrieved by importer2.py (above), these images can be combined into a move (again using
ImageMagick or other graphical tool) to a movie of how the map's appearance changed. 

LICENSE:

These programs are licensed under a Creative Commons Attribution-ShareAlike 3.0 
Unported License (http://creativecommons.org/licenses/by-sa/3.0/) 

To attribute this work, place a link to http://intermapper.com in the Credits or About...
window of your software. We would love to have you send any changes to the code 
back to us at support@intermapper.com.
