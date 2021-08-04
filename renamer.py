import time
import os
path = "C:/Users/granc/Documents/Paradox Interactive/Victoria II/GFM/save games"
while True:
    dirs = os.listdir( path )
    for file in dirs:
        if file == "autosave.v2":
            try:
                os.rename(path+'/autosave.v2',path+"/"+str(len(dirs))+".v2")
            except:
                pass
    time.sleep(2)
    print(dirs)