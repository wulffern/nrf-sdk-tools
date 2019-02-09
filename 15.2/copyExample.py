# Copyright (c) 2019 wulff
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import sys
import shutil
import glob
import re



def copyPath(fromPath,toPath):
    if(os.path.exists(toPath)):
        print(f"Error: path {toPath} already exists.")
    else:  
        shutil.copytree(fromPath,toPath)

def removeOtherThanSegger(path):
    #subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    
    dirList  = glob.glob(f"{path}/**/",recursive=True)
    
    dirsToDelete = [folder for folder in dirList if re.search(r"arm|iar|Output",folder)]
    for d in dirsToDelete:
        if(os.path.exists(d)):
            shutil.rmtree(d) 

def modifySeggerProject(filename):
    if(not os.path.exists(filename)):
        raise Exception(f"Could not find {filename}")
    shutil.copy(filename,f"{filename}.bak")
    print(filename)
    buffer = ""
    with open(filename,"r") as f:
        for line in f:
            #print(line)
            m = re.search(r"c_user_include_directories=\"(.*);\"",line)
            if(m):
                includes = str(m.groups(1))
                dirs = includes.split(";")
                for d in dirs:
                    print(d)
                #for i in range(1,len(m):
                #print(m)
                

    #print(buffer)

        

def findAndModifySeggerProject(path):
    sesProjects  = glob.glob(f"{path}/**/*.emProject",recursive=True)
    for f in sesProjects:
        modifySeggerProject(f)

def main(fromPath, toPath):
    #copyPath(fromPath,toPath)
    #removeOtherThanSegger(toPath)
    findAndModifySeggerProject(toPath)




if(len(sys.argv) == 3):
    main(sys.argv[1],sys.argv[2])
else:
    print(len(sys.argv))
    print("Usage: copySeggerExample.py <fromPath> <toPath>")