#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import collections
import os
from git import Repo

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
    """
    result = []
    #get a list of username
    for row in table:
        if row[2].strip() != '':
            result.append(row[2].strip() 
    return result 


def cloneRepos(hwName,data):
    """
    hwName: homework name, it's also the general folder name per hw.
    data: one column list of github username

    return a dict, {username:if clone success}
    """
    
    #check if there's hwName folder,if there's not, create one
    hwfolder = os.path.join(hwRF,hwName)
    if not os.path.isdir(hwfolder):
        os.mkdir(hwfolder)

    for username in data:
        #compose git url for each username in a list
        giturl = 'https://github.com/'+username+'/'+hwName+'.git'
        targeturl = os.path.join(hwfolder,username+'-'+hwName)
        repo = Repo.clone_from(giturl, targeturl, branch='master')
        
    

    #clone url one by one, check if success, store all repo obj in a list
    
    
    
    
if __name__ == "__main__":

    loadcsv('prepared.csv')
    
    namelist = getNameList() 

    
    
        
        

    
