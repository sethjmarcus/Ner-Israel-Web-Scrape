import prtpy
import os
from pathlib import Path

path = '/media/seth/SETH_BACKUP/testing/'
sub_folder = 'Moreinu HaRav Yaakov Moshe Kulefsky/'
files = list(os.listdir(path + sub_folder))

theDict = dict()
for something in files: #Calculate size for all files here. 
    theDict[something] = os.stat(path+sub_folder+something).st_size #theStats

#for item in theDict:
#    print("The File: {:30s} The Size: {:d} Bytes".format(item,theDict[item]))

result = prtpy.pack(algorithm=prtpy.packing.first_fit, binsize=700000000, items=theDict)

for idx, x in enumerate(result):
    mypath = path + str(idx) + "/"
    if not os.path.isdir(mypath):
        os.makedirs(mypath)
    
    for item in x:
        old_file = path + sub_folder + item
        new_file = mypath + item
        #print(old_file, new_file)
        os.replace(old_file, new_file)
