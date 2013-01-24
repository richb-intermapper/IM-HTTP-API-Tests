# http://www.gossamer-threads.com/lists/python/python/652793?page=last
import threading
import time
import urllib

# Using imagemagick to create an animated GIF like this:
#
#    convert   -delay 20   -loop 0   immaps/*.jpg   animatedmap.gif

def repeat(event, every, action):
    while True:
        action()
        event.wait(every)
        if event.isSet():
            break

def foo():
#    aDate = time.strftime("%H:%M", time.localtime())
    aDate = time.strftime("%Y-%b-%d_%H-%M-%S",time.localtime())
    print "HTTP GET image at %s..." % aDate
    (fname, hdrs) = urllib.urlretrieve('https://192.168.1.127/g4cef4173/document/main/*map.jpeg',
                                   '/home/dartware/Documents/immaps/%s.jpg' % aDate)

print "Retrieve successive map's images from InterMapper"

print "creating event and thread"
ev = threading.Event()
t1 = threading.Thread(target=repeat, args=(ev, 60*5, foo))
print "starting thread"
t1.start()

print "starting main thread; end in 24 hours"
try:
    time.sleep(60*60*24) # stop after 24 hours
except KeyboardInterrupt:
    print " Keyboard interrupt!"
else:
    print "setting event because time has run out"
ev.set()
print "waiting for thread to finish"
t1.join()
print "quit"
