# Program to retrieve background images from CodeFromThe70s.org
# Three separate threads: 
#   - one to retrieve image via HTTP. Runs every 20 minutes for politeness to his server
#   - one to use IM HTTP API to push wallpaper & icon files into the Backgrounds and Default folders
#   - one to retrieve current weather map from weather.com

# not much error handling: os errors will halt the program I'm pretty sure. Uses a lock to mediate access
# to the graphic being retrieved/imported.
# 30 Nov 2010 -reb
# 07 Dec 2010 -reb
# 16 Oct 2011 -reb Tweaked to run on OSX to see if IM 5.4.x would create a folder if it's specified in URL. Yes.

# http://www.gossamer-threads.com/lists/python/python/652793?page=last
import threading
import time
import os
import urllib

curlwallpaper = 'curl -k -s --data-binary "@wallpaper-time.jpg" https://127.0.0.1/~files/icons/JUMBLE/bgwallpaper.jpg'
curlicon      = 'curl -k -s --data-binary "@time-icon.png"      https://127.0.0.1/~files/icons/Default/time-icon.png'
curlwxmap     = 'curl -k -s --data-binary "@wxmap.jpg"          https://127.0.0.1/~files/icons/JUMBLE/Backgrounds/wxmap.jpg'

imgmgktime = "convert ./wallpaper.jpg -fill white -undercolor '#00000080' -gravity SouthEast -annotate +0+5 ' %s ' wallpaper-time.jpg"
imgmgkicon = "convert -background lightblue -fill blue -pointsize 36 label:'%s' time-icon.png"

# This URL returns a JPEG when it is given a UTC timestamp at the end, like this ...&utc=129046401
wallpaperURL = 'http://www.codefromthe70s.org/cgi/desktopearthgen.exe?width=1280&height=768&center=5&bars=1&clouds=1&utc=%s'
wxmapURL     = 'http://image.weather.com/images/maps/current/curwx_600x405.jpg'

def repeat(event, every, action):
    while True:
        action()
        event.wait(every)
        if event.isSet():
            break

# Thread to send the timestamped wallpaper, icon, & weather map images to IM via HTTP
def importer():
    aDate = time.strftime("%Y-%b-%d_%H-%M-%S",time.localtime())
    aTime = time.strftime("%H:%M")
    print "HTTP POST'ing all images to IM at %s..." % (aDate)

# generate the updated icon file
    retcode = os.system(imgmgkicon % aTime) 

    imgLock.acquire()
    retcode = os.system("%s  > /dev/null" % (curlwallpaper)) # send wallpaper
    retcode = os.system("%s  > /dev/null" % (curlicon))      # send icon
    retcode = os.system("%s  > /dev/null" % (curlwxmap))     # send weathermap
    imgLock.release()

# Thread to retrieve Desktop Earth image, time stamp it with the date
def retriever():
    aDate = time.strftime("%Y-%b-%d_%H-%M-%S",time.localtime())
    aDateSecs = str(int(time.time()))
    print "Retrieving wallpaper image at %s..." % (aDate)
# Retrieve the image from CodeFromThe70s
# acquire lock for the image file
    imgLock.acquire()
#    print wallpaperURL % aDateSecs
    (fname, hdrs) = urllib.urlretrieve(wallpaperURL % aDateSecs, '/Users/richb/Documents/src/HTTP API Tests/wallpaper.jpg')
# update the image by adding the time stamp into the lower-right corner of the image using ImageMagick
#    print imgmgkcmd % aDate
    retcode = os.system(imgmgktime % aDate)
    imgLock.release()

# Thread to retrieve weather map and save it
def retrieveWxMap():
    aDate = time.strftime("%Y-%b-%d_%H-%M-%S",time.localtime())
    print "Retrieving weathermap image at %s..." % (aDate)
# Retrieve the image from Weather.com
# acquire lock for the image file
    imgLock.acquire()
    (fname, hdrs) = urllib.urlretrieve(wxmapURL, '/Users/richb/Documents/src/HTTP API Tests/wxmap.jpg')
    imgLock.release()

# Create the lock to control access to the image
imgLock = threading.Lock()

print "creating thread to retrieve the wallpaper image"
ev1 = threading.Event()
retrievalThread = threading.Thread(target=repeat, args=(ev1, 60*20, retriever))
print "starting it"
retrievalThread.start()

print "creating thread to retrieve the weather map image"
ev2 = threading.Event()
retrievalThread2 = threading.Thread(target=repeat, args=(ev2, 60*5, retrieveWxMap))
print "starting it"
retrievalThread2.start()

print "creating thread to HTTP POST it into InterMapper"
ev = threading.Event()
importThread = threading.Thread(target=repeat, args=(ev, 60.0, importer))
print "starting it"
importThread.start()

print "starting main thread; end in 24 hours"

try:
    time.sleep(60*60*24) # stop after 24 hours
except KeyboardInterrupt:
    print " Keyboard interrupt"
else:
    print "setting event because time has run out"
ev.set()
ev1.set()
ev2.set()

print "waiting for threads to finish"
importThread.join()
retrievalThread.join()
print "quit"
