#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import collections
import os
import git
import shutil

homefolder = os.path.expanduser("~")
hwRF = os.path.join(homefolder,'homeworks') #homework root folder name

namelist =[]   

#input [id,name,githubid,unkonwn]
table = []
lectureTable = []


def loadcsv(filename):
    """
    load prepared csv file
    """
    with open(filename,'r') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='|')      
        for row in csvreader:
            table.append(row)

def writeResultCSV(hwName,data):
    with open(hwName+'.csv','w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|')
        csvwriter.writerow(['Name','DownloadStatus'])
        for key,value in data.items():
            #value is list, key is the real name.
            csvwriter.writerow([key] + value)
            

def writecsv(data, filename):
    """
    write output csvfile
    data is a dict
    """
    with open(filename,'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter='|')
        csvwriter.writerow(["ID","name","githubID","hw1","hw2","hw3","hw4","hw5","finalW"])
        for key,value in data.items():
            
            #value changed, so change output
            if type(value) != type([]):
                csvwriter.writerow([unicode(key,"utf-8"),value])
            else:    
                #write as is
                rowlist = [key]
                csvwriter.writerow(rowlist+value)            
                    
def getNameList():
    """
    using raw table data return a list of username
    [real name, github username]
    """
    result = []
    #get a list of username
    for row in table:
        if (len(row) >= 2) and (row[1].strip() != ''):
            if row[2].strip() != '':
                result.append([row[1].strip(),row[2].strip()])
            else:
                result.append([row[1].strip(),None])
        
    return result 


def cloneRepos(hwName,data):
    """
    hwName: homework name, it's also the general folder name per hw.
    data: one column list of github username

    return a ordered dict, {username:if clone success}
    """
    
    #check if there's hwName folder,if there's not, create one
    hwfolder = os.path.join(hwRF,hwName)
    if not os.path.isdir(hwfolder):
        os.mkdir(hwfolder)
    
    repolist = []
    #clone url one by one, check if success, store all repo obj in a list
    for row in data:
        username = row[1] 
        #compose git url for each username in a list
        giturl = 'https://github.com/'+username+'/'+hwName+'.git'
        targeturl = os.path.join(hwfolder,username+'-'+hwName)
        
        #remove dir if exists, otherwise causing problem with GitPython
        if (os.path.isdir(targeturl)):
            print "Warning, path already exists on %s remove it or skip?(y/n)" % targeturl
            if (raw_input() == 'y'):
                print "Removing..."
                shutil.rmtree(targeturl)
                print "Removed"
            else:
                print "Skip."
                continue 
    
        try:
            repo = git.Repo.clone_from(giturl, targeturl, branch='master')
        except git.exc.InvalidGitRepositoryError:
            #git url not reachable
            print "Given GitHub url is not reachable, %s" % giturl 
        except git.exc.NoSuchPathError:
            print "Local path %s does not exist." % targeturl
        except git.exc.GitCommandError:
            print "Git command execution proble."
        
        #check if repo created successfully
        if (os.path.isdir(targeturl)):
            repolist.append(repo)
        else:
            repolist.append('')

    result = collections.OrderedDict() 
    i = 0
    for r in repolist:
        if r != '':
            #data[i] is one row, data[i][0] is the real name
            result[data[i][0]] = [data[i][1],True]
        else:
            result[data[i][0]] = [data[i][0],False]
        i++

    return result


    
    
    
    
if __name__ == "__main__":

    targetHWname = 'homeworkone'     
    loadcsv('prepared.csv')
    
    #two colmn 
    namelist = getNameList() 

    cloneResult = cloneRepos(targetHWname,namelist)

    #write result csv here
    writeResultCSV(targetHWname,cloneResult)
    

    

    
    
        
        

    
