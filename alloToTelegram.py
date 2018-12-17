from os import listdir
from os.path import isfile, join

print ('starting tool')
myPath = r'C:\Users\David\Documents\GitHub\Allo-to-Telegram-tool\alloCSV';

fileList = [f for f in listdir(myPath) if isfile(join(myPath, f))]

for names in fileList:
    print (names)
    
    file currentBackup = open(names, r, -1)

def file_processing:
    print ("processing conversation ")
def telegram_writer:
    print ("begin writing")