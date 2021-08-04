#to be used when you play a game of Victoria 2 and do not make manual saves, instead relying on autosaves as to not mess up the numbering
#setting autosaves to every half year or every one year I have found to be the sweet spot
#every x seconds check if autosave.v2 exists, if so rename it "number of files in save games folder".v2

import time
import os
path = "C:/Users/robert/Documents/Paradox Interactive/Victoria II/GFM/save games" # change path to where autosaves are created
while True:
    dirs = os.listdir( path )
    for file in dirs:
        if file == "autosave.v2":
            try:
                os.rename(path+'/autosave.v2',path+"/"+str(len(dirs))+".v2")
            except:
                pass
    time.sleep(2) #check folder every this number seconds
    print(dirs)
