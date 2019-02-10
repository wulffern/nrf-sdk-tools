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
        raise Exception(f"Error: path {toPath} already exists.")
    else:  
        shutil.copytree(fromPath,toPath)

def removeOtherThanSegger(path):
    #subdirs = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
    
    dirList  = glob.glob(f"{path}/**/",recursive=True)
    
    dirsToDelete = [folder for folder in dirList if re.search(r"arm|iar|Output",folder)]
    for d in dirsToDelete:
        if(os.path.exists(d)):
            shutil.rmtree(d) 

def getRemoteOrLocalPath(sdkPath,currentSeggerFileLocation,originalSeggerFileLocation,path):
    #- Try local first
    newPath = ""
    localPath = os.path.normpath(currentSeggerFileLocation + "/" + path)
    remotePath = os.path.abspath(originalSeggerFileLocation + "/" + path)
       
    if(os.path.exists(localPath)):
        newPath = path
    elif(os.path.exists(remotePath)):   
        newPath = remotePath

    newPath = newPath.replace(sdkPath,"$(SDK)")
    return newPath


def modifySeggerProject(sdkPath,projectPath,copiedPath,filename):
    if(not os.path.exists(filename)):
        raise Exception(f"Could not find {filename}")
    shutil.copy(filename,f"{filename}.bak")
    originalSeggerFileLocation = os.path.dirname(os.path.normpath(projectPath + str(filename).replace(copiedPath,"")))
    currentSeggerFileLocation = os.path.dirname(filename)
    buffer = ""
    with open(filename,"r") as f:
        for line in f:
            
            #- Replace include directories
            includeDirRegex = r"c_user_include_directories=\"(.*);\""
            m = re.search(includeDirRegex,line)
            if(m):
                includes = str(m.group(1))
                dirs = includes.split(";")
                paths = ""
                for d in dirs:
                    newPath = getRemoteOrLocalPath(sdkPath,currentSeggerFileLocation,originalSeggerFileLocation,d)
                    if(newPath != ""):
                        paths += newPath + ";"
        
                line = re.sub(includeDirRegex,f"c_user_include_directories=\"{paths}\"",line)
            
            #- Replace file_names that have a "../../<path>" pattern
            fileNameRegex = r"\"(../../.*)\""
            mfile = re.search(fileNameRegex,line)
            if(not m and mfile):
                newPath = getRemoteOrLocalPath(sdkPath,currentSeggerFileLocation,originalSeggerFileLocation,mfile.group(1))   
            
                if(newPath != ""):
                    line = re.sub(fileNameRegex,f"\"{newPath}\"",line)
            

            #if(re.search(r"</solution>",line)):
            #    line = f"<configuration  Name=\"Common\" environment_variables=\"nRF5_SDK_DIR = {sdkPath}\" />\n" + line
            #- Gobble up lines
            buffer += line + "\n"
                
     
    with open(filename,"w") as f:
        f.write(buffer)

        

def findAndModifySeggerProject(sdkPath,projectPath,path):
    sesProjects  = glob.glob(f"{path}/**/*.emProject",recursive=True)
    for f in sesProjects:
        modifySeggerProject(sdkPath,projectPath,path,f)

def main(sdkPath,fromPath, toPath):
    print(f"Copying {fromPath} to {toPath}")
    copyPath(fromPath,toPath)
    print(f"Removing non Segger Embedded Studio Projects")
    removeOtherThanSegger(toPath)
    print(f"Modifying paths in Segger Embedded Studio Projects")
    projectPath = os.path.normpath(f"{fromPath}/")

    findAndModifySeggerProject(os.path.abspath(sdkPath),projectPath,toPath)




if(len(sys.argv) == 4):
    main(sys.argv[1],sys.argv[2],sys.argv[3])
else:
    print("Usage: copyExample.py <SDK base dir> <from path> <to path> ")