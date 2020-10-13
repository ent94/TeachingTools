import pandas as pd
import numpy as np

def accessBB(url):
    """Return the raw data from Blackboard."""
    rawdata = pd.DataFrame([['Student 1',68,100,95,98],['Student 2',98,'-',76,54]],columns=['name','PreLab1','Lab1','PreLab2','Lab2'])
    return rawdata

def prettyAssignment(studentnames,assignnames,rawData):
    """Return the list of grades or missing submissions from the data for one specific assignment."""
    listofnames = pd.DataFrame(rawData[studentnames])
    listofinformation = pd.DataFrame(rawData[assignnames])
    data = pd.concat([listofnames, listofinformation], axis=1, sort=False)
    return data

def sectionstats(rawData):
    """Return a list of descriptive stats for one section."""
    # I want this function to print a list of states about my sections
    # I am not sure exactly what I want from my sections yet and I think this is going to depend
    # on how I set up the earlier functions and what I can actually manage
    return 0

def missingassignments(rawData):
    """Return a list of students and their missing assignments."""
    l = []
    for i in range(len(rawData['name'])):
        for j in rawData.columns:
            if rawData.iloc[i][j] == '-':
                l.append([rawData.iloc[i]['name'],j])
    return l