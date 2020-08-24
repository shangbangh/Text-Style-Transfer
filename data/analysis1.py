'''
Created on May 27, 2020

@author: myuey
'''
import os 
import shutil
import nltk
from textblob import TextBlob
import time
from nltk.tokenize import sent_tokenize

def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
#creates folders containing the requested count of files from a target folder
def batch(batchCount, folderIn, folderBase):
    files = os.listdir(folderIn)
    folderInd = 0
    fileInd = 0
    curTarget = folderBase + str(folderInd) + "/"
    create_folder(curTarget)
    for fname in files:
        if fileInd < batchCount:
            shutil.copy(folderIn + fname, curTarget + fname)
        else:
            fileInd = 0
            folderInd += 1
            curTarget = folderBase + str(folderInd) + "/" 
            create_folder(curTarget) 
            shutil.copy(folderIn + fname, curTarget + fname)
        fileInd += 1

def mass_rename(folderIn, folderOut, prefix, startInd, endInd):
    #Renames and copies all files in a folder to a target folder 
    #by adding the provided string as a prefix to their filenames
    files = sorted_listdir(folderIn, startInd, endInd)
    for fname in files:
        shutil.copy(folderIn + fname,folderOut)
        os.rename(folderOut+fname, folderOut + prefix + fname)


def text_comp(fileComp, fileBase):
    #analyzes given text file against a baseline text file for differences 
    #returns number of differences found
    #TODO
    baseStr = ""
    with open(fileBase, encoding = 'utf-8') as f:
        baseStr = f.read()
    #open comparison file
    compStr = ""
    with open(fileComp, encoding = 'utf-8') as f2:
        compStr = f2.read()
    #create textblobs for each
    tblo_base = TextBlob(baseStr)
    tblo_comp = TextBlob(compStr)

    #split tblos into sentences
    
    #compare if sentences are the same
    
    #if not, loop through word by word to find difference
    
    #once difference is found, 
    
#minsize in kb
#returns list of files in folder that are smaller than the minimum size
def file_size_check(folder, minSize):
    files = os.listdir(folder)
    res = []
    for fname in files:
        fSize = os.path.getsize(folder + fname)
        if(fSize / 1024 < minSize):
            res.append(fname)
    return res 
#minsize in kb
#returns any files in the folder pair off that are mismatched
def file_size_comp(machFolder, humFolder, mismatchVal, startInd, endInd):
    machFiles = sorted_listdir(machFolder, startInd, endInd)
    humFiles = sorted_listdir(humFolder, startInd, endInd)
    result = []
    fileInd = 0
    for fname in machFiles:
        mSize = os.path.getsize(machFolder + fname) / 1024
        hSize = os.path.getsize(humFolder + humFiles[fileInd]) / 1024
        if abs(hSize - mSize) > mismatchVal:
            result.append(fname) 
    return result
#returns list of all unique words and punctuation in the files of a folder
def vocab(folder):
    files = os.listdir(folder)
    resStr = []
    for fname in files:
        with open(folder + fname, encoding = 'utf-8') as f:
            resStr.append(f.read())
    tblo = TextBlob("".join(resStr))
    wordlist = []
    for word in tblo.tokens:
        if(not (word in wordlist)):
            wordlist.append(word)
    return wordlist
#returns list of words and punctuation of a text string
def getTokens(inputList):
    tblo = TextBlob("".join(inputList))
    resList = []
    for word in tblo.tokens:
        resList.append(word)
    return resList
#writes a list to a file
def write_list(listname,file):
    with open(file, encoding = 'utf-8', mode = 'w') as f:
        f.write(", ".join(listname))
#returns word count of a file
def wordcounter(file):
    with open(file, encoding = 'utf-8') as f:
        res = f.read()
    tblo = TextBlob(res)
    return len(tblo.tokens)
#returns max number of words in a file in a folder
def folder_max_word(folder):
    filelist = os.listdir(folder)
    numCheck = 0
    for file in filelist:
        numWords = wordcounter(folder + file)
        if(numWords > numCheck):
            numCheck = numWords
    return numCheck
#trims tab and multiple space whitespace from all files in a folder, and puts them in a target folder
def trim(folderIn,folderOut):
    files = os.listdir(folderIn)
    for fname in files:
        with open(folderIn + fname, encoding = 'utf-8') as f:
            content = f.read()
        content.replace('\t', '')
        content.replace('  ', ' ')
        content.replace('   ', ' ')
        with open(folderOut + fname, mode = 'w', encoding = 'utf-8') as f2:
            f2.write(content)

#counts sentences of files in two folders, 
#they should have the same number of files and have the same filenames for each chapter
def sentencecountchecker():
    nltk.download('punkt')
    machFolder = "./machTransData/"
    humFolder = "./testHumData/"
    
    machFiles =  os.listdir(machFolder)
    res = []
    for file in machFiles:
        #pull text file into string
        with open(machFolder + file, encoding = 'utf-8') as f:
            resMach = f.read()
        with open(humFolder + file, encoding = 'utf-8') as f:
            resHum = f.read()
        #separate by newline
        machSplit = resMach.split('\n')
        humSplit = resHum.split('\n')
        #pull titles
        #machTitle = machSplit[0]
        #humTitle = humSplit[0]
        #remove titles from string
        machBody = "".join(machSplit[1:])
        humBody = "".join(humSplit[1:])
        #count sentences
        machCount = len(sent_tokenize(machBody))
        humCount = len(sent_tokenize(humBody))  
        if(machCount != humCount):
            resStr = file + " M: " + str(machCount) + " H: " + str(humCount)
            res.append(resStr)
    return res
#counts the number of unique characters used
def char_count_uni(file):
    with open(file, encoding = 'utf-8') as f:
        fileString = f.read()
    return len(set(fileString))

#adds START_ and _END tags to all files in the folder, and writes the result to a different folder
#use this on the human translated files
def human_tag(folderIn, folderOut, startInd, endInd, firstChap, lastChap):
    files = sorted_listdir(folderIn, startInd, endInd)  
    chapInd = firstChap
    while chapInd < lastChap + 1:
        resStr = []
        resStr.append("START_ ")
        with open(folderIn + files[chapInd - 1], encoding = 'utf-8') as f:
            resStr.append(f.read())
        resStr.append(" _END")
        outStr = "".join(resStr)
        with open(folderOut + files[chapInd - 1], mode = 'w', encoding = 'utf-8') as f2:
            f2.write(outStr)
        chapInd +=1
                
#merges text files in a folder to a new text file
def text_merge_folder(folder, file, startInd, endInd):
    files = sorted_listdir(folder, startInd, endInd)
    resStr = []
    for fname in files:
        with open(folder + fname, encoding = 'utf-8') as f:
            resStr.append(f.read())
            resStr.append("\n")
    with(open(file,mode = 'w', encoding = 'utf-8')) as newfile:
        newfile.write("".join(resStr))
#merges a list of text files together into a new text file
def text_merge_list(listofFiles, file):
    resStr = []
    for fname in listofFiles:
        with open(fname, encoding = 'utf-8') as f:
            resStr.append(f.read())
            resStr.append("\n")
    with(open(file,mode = 'w', encoding = 'utf-8')) as newfile:
        newfile.write("".join(resStr))
#returns a list containing all words in a chapter folder, indexed by chapter order
def wordlist(folder):
    resStr = []
    files = os.listdir(folder)
    for fname in files:
        with open(folder + fname, encoding = 'utf-8') as f:
            resStr.append(f.read())
    return resStr
#counts the characters of all files in a folder
def char_counter(folder):
    res = 0
    files = os.listdir(folder)
    for fname in files:
        with open(folder + fname, encoding = 'utf-8') as f:
            contents = f.read()
            res += len(contents)
    return res        
#returns a sorted list of files/directories in a directory, sorted by chapter number
def sorted_listdir(folder, startInd, endInd):
    #pull listdir
    dirIn = os.listdir(folder)
    #create dict
    dictIn = {}
    #loop through dir, pull key from title, then add to dict
    for file in dirIn:
        keyInd1 = file.find(" ")
        keyInd2 = file.find(".t")
        keyInt = int(file[keyInd1:keyInd2])
        dictIn[keyInt] = file
    resList = []
    #loop through index range, building sorted list
    while startInd < endInd + 1:
        fileName = dictIn[startInd]
        resList.append(fileName)
        startInd += 1
    return resList
#merges files in the targeted folder to the given file name using the provided tag to mark separations
def text_merge_tag(folder, file, tag, startInd, endInd):
    files = sorted_listdir(folder, startInd, endInd)
    resStr = []
    fileInd = 0
    for fname in files:

        with open(folder + fname, encoding = 'utf-8') as f:
            resStr.append(f.read())
            resStr.append("\n")
            resStr.append(tag)
            resStr.append("\n")
                

        fileInd += 1
        
    with(open(file,mode = 'w', encoding = 'utf-8')) as newfile:
        newfile.write("".join(resStr))
#splits given file into the target folder, breaking on tags. Will use indices on naming new files
def text_split_tag(folder, file, tag, startInd, fileBase):
    #read file into string
    with open(file, encoding = 'utf-8') as f:
        resStr = f.read()
    indTag = resStr.find(tag)
    while indTag != -1:
        #pull first part of input to first found tag
        res_split = resStr[:indTag]
        #create file to save to
        chapName = folder + fileBase + str(startInd) + ".txt"
        with open(chapName, encoding = 'utf-8', mode = 'w') as f2:
            f2.write(res_split)
        #reset string, tag index
        resStr = resStr[indTag + len(tag):]
        indTag = resStr.find(tag)
        #update index
        startInd+=1  
    
def file_same_check(file1, file2):
    with open(file1, encoding = 'utf-8') as f:
        resStr1 = f.read()    
    with open(file2, encoding = 'utf-8') as f:
        resStr2 = f.read()      
    return resStr1.strip() == resStr2.strip()

def folder_file_same_check(folder1,folder2, startInd, endInd):
    files1 = sorted_listdir(folder1, startInd, endInd)
    files2 = sorted_listdir(folder2, startInd, endInd)
    fileInd = 0
    resArr = []
    for file in files1:
        fileComp = files2[fileInd]
        compRes = file_same_check(folder1 + file,folder2 + fileComp)
        if not compRes:
            resArr.append(file)
        fileInd +=1
    return resArr
#returns the position of the first difference between 2 strings and a specified number of 
#characters before or after that point for string 1
def find_diff_string(string1, string2):
    #set return range before/after divergence point
    retRange = 5
    #set chkstrings based on which one is shorter
    firstFlag = len(string1) < len(string2)
    if firstFlag:
        chkStr1 = string1
        chkStr2 = string2
    else:
        chkStr1 = string2
        chkStr2 = string1
    chInd = 0
    resStr = ""
    posType = ">_>"
    for ch1 in chkStr1:
        ch2 = chkStr2[chInd]
        if ch1 != ch2:
            #point of divergence found
            #determine if return range will be before or after point
            if chInd + retRange > len(chkStr1) or chInd + retRange > len(chkStr2):
                #use before
                startInd = chInd - retRange
                resStr += chkStr1[startInd:chInd]
                posType = "before"
            else:
                #use after
                endInd = chInd + retRange
                resStr += chkStr1[chInd:endInd]
                posType = "after"
            break
        chInd += 1
    if firstFlag:
        return "str1",chInd,resStr,posType
    else:
        return "str2",chInd,resStr,posType
#checks the total number of characters in a folder's files and will split it into smaller folders if total is over 1 million.
#does nothing otherwise
def folder_split(folderTarget, folderBase, startInd, endInd):
    fileList = sorted_listdir(folderTarget, startInd, endInd)
    maxChar = 325000
    charCount = char_counter(folderTarget)
    print(charCount)
    print(len(fileList))
    if charCount > maxChar:
        totCharCount = 0
        folderInd = 0
        folderSect = []
        for file in fileList:
            with open(folderTarget + file, encoding = 'utf-8') as f:
                contents = f.read()
                fileChar = len(contents)
            if totCharCount + fileChar < maxChar:
                #add this file to current section of folder
                folderSect.append(file)
                totCharCount += fileChar
                print(file)
            else:
                #create new folder with current section
                print(folderSect)
                create_folder(folderBase+ str(folderInd))
                for fileName in folderSect:
                    shutil.copy(folderTarget + fileName, folderBase + str(folderInd) + "/" + fileName)
                #reset section and character count
                folderSect = []
                totCharCount = 0
                folderInd += 1
                #add current file to new folderSect
                folderSect.append(file)
                totCharCount += fileChar
        #create fianl foldersect
        print(folderSect)
        create_folder(folderBase+ str(folderInd))
        for fileName in folderSect:
            shutil.copy(folderTarget + fileName, folderBase + str(folderInd) + "/" + fileName) 

    
