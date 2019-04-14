import os, os.path

for root, _, files in os.walk("/app/kafka/logs/"):
    for f in files:
        fullpath = os.path.join(root, f)
        try:
            if os.path.getsize(fullpath) > 1024 * 1024 * 1024:   #set file size in kb
                print fullpath
                os.remove(fullpath)
        except Error:
            print "Error" + fullpath
