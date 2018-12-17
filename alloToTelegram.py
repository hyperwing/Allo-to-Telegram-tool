from os import listdir
from os.path import isfile, join

print ('starting tool')
myPath = r'C:\Users\David\Documents\GitHub\Allo-to-Telegram-tool\alloCSV';

fileList = [f for f in listdir(myPath) if isfile(join(myPath, f))]

for name in fileList:
    print (name)
    
    currentBackup = open(name, "r")
    file_processing(name)

def file_processing:
    print ("processing conversation ")
def telegram_writer:
    print ("begin writing")