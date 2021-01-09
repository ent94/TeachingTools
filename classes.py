"""
Calculate, Organize, and Display useful information when teaching a course with multiple sections.

View information about individual students, assignments, and sections as well as overall course informtion
 across all sections.

...

Classes
-------
student()
    Calculate and display information about an individual student
assignment()
    Calculate and display information about an individual assignment
course()
    Load in all data and compile/display course wide information
section()
    Calculate and display information about an individual section
"""
import pandas as pd
import os
from functions import determine_grade
import json


class student():
    """
    A class to represent a student.
    
    ...
    
    Attributes
    ----------
    uname : str
        Student username
    gradesD : dict
        key = assignment name, str and entry = grade, float
    nosub : lst
        list of unsubmitted assignments, str
    needsgrade : lst
        list of ungraded assignments, str
    allPer : float
        grade percentage including all possible assignments
    allLet : str
        letter grade including all possible assignments
    shortPer : float
        percentage excluding ungraded and unsubmitted assignments
    shortLet : str
        letter grade excluding ungraded and unsubmitted assignemnts
    """
    
    def __init__(self, username, ptsDict, sectDF):
        """
        Compiles and calculates all necessary information about the student object.
        
        Parameters
        ----------
            username : str
                username of the student
            ptsDict : dict
                key = assignment name, str and entry = points possible, float
            sectDF : DataFrame
                all data for the section with username as key
        """
        self.uname = username
        
        nosub = []
        needsgrade = []
        shortL = []
        gradesD = {}
        stuPts = 0
        shortPoss = 0
        longPoss = 0

        for i in list(ptsDict.keys()):
            gtemp = sectDF.at[username, i]
            possPts = ptsDict[i]
            longPoss += possPts
            if gtemp == 'No Submission':
                nosub.append(i)
            elif gtemp == 'Needs Grading':
                needsgrade.append(i)
            else:
                gtemp = float(gtemp)
                stuPts += gtemp
                shortPoss += possPts
            gradesD[i] = gtemp

        if needsgrade == []:
            needsgrade.append('No assignments need grading')
        if nosub == []:
            nosub.append('All assignments have been submitted')

        self.gradesD = gradesD
        self.nosub = nosub
        self.needsgrade = needsgrade
        allPer = (stuPts/longPoss)*100
        self.allPer = allPer
        self.allLet = determine_grade(allPer)
        shortPer = (stuPts/shortPoss)*100
        self.shortPer = shortPer
        self.shortLet = determine_grade(shortPer)

    def __str__(self):
        # This will eventually print useful information about the student
        rope = 'This is what comes out of print(student)'
        return rope


class assignment():
    """
    A class to represent an assignment.
    
    ...
    
    Attributes
    ----------
    aname : str
        Assignment name
    avgper : float
        average assignment percentage in the section without needs grading, 
        no submission, or 0's
    avglet : str
        average assignment letter grade (based on avgper) in the section
    needsgrade : lst
        list of usernames, str, in the section that need grading for the assignment
    nosub : lst
        list of usernames, str, in the section that have not submitted the assignment
    """
    
    def __init__(self, aname, stuL, ptsDict, sectData):
        """
        Compiles and calculates all necessary information about the assignment object.
        
        Parameters
        ----------
        aname : str
            name of the assignment
        stuL : lst
            list of usernames, str, in the section
        ptsDict : dict
            key = assignment name, str and entry = points possible, float
        sectData : DataFrame
            all data for the section with username as key
        """
        self.aname = aname

        pts = ptsDict[aname]
        needsgrade = []
        nosub = []
        nstu = 0
        tot = 0

        for i in stuL:
            grade = sectData.at[i, aname]
            if grade == 'Needs Grading':
                needsgrade.append(i)
            elif grade == 'No Submission':
                nosub.append(i)
            elif float(grade) == 0:
                continue
            else:
                nstu += 1
                tot += float(grade)

        if pts == 0:
            p = ['This is an extra credit assignment. No average score is needed']
            let = ['This is an extra credit assignment. No letter is given']
        else:
            p = (tot/nstu)/pts*100
            let = determine_grade(p)
        if needsgrade == []:
            needsgrade.append('All submitted assignments have been graded')
        if nosub == []:
            nosub.append('All assignments have been submitted')

        self.avgper = p
        self.avglet = let
        self.needsgrade = needsgrade
        self.nosub = nosub

        # ***I never give anyone a straight up 0***
        # ***I only put a 0 in when a student has not submitted something and has no intent to***
        # ***I don't want them in my average because they don't represent real student work***
        # ***I think it's really only useful to compare to real student work here***

    def __str__(self):
        # This will eventually print useful information about the assignment
        rope = 'This is what comes out of print(assignment)'
        return rope


class course():
    """
    A class to represent an entire course.
    
    ...
    
    Attributes
    ----------
    cname: str
        Course name
    avgG : float
        average student percentage grade
    snumsL : lst
        list of section numbers, str
    allstu : lst
        list of all student usernames, str
    masterassnL : lst
        list of all assignments, str, across all sections
    sectD : dict
        key = section number, str and entry = section, class object
    sectusers : dict
        key = section number, str and entry = usernames, str, in lists
    sectgrades : dict
        key = section number, str and entry = average student grade, float
    assnsectnumD : dict
        key = assignmnet name, str and entry = section numbers, str, that have that assignment in lists
    assncourseavgD : dict
        key = assignment name, str and enrtry = averge score across all sections, float
    """
    
    def __init__(self, directory):
        """
        Compiles and calculates all necessary information about the course object.
        
        Parameters
        ----------
        directory : str
            directory with location of .txt data files
        """
        self.cname = directory[-7:-1]

        dictionary = {}
        sectusers = {}
        sectassn = {}
        sectgrades = {}
        assngrades = {}
        listofsections = []
        allstuL = []
        totG = 0

        # Create all section objects and store them in a dictionary
        for i in sorted(os.listdir(directory)):
            sectionnumber = i[i.find('_')+1:len(i)-4]
            listofsections.append(sectionnumber)
            tempsect = section(sectionnumber,os.path.join(directory, i))
            dictionary[sectionnumber] = tempsect
            sectusers[sectionnumber] = tempsect.stuL
            allstuL.extend(tempsect.stuL)
            sectassn[sectionnumber] = tempsect.assignL
            sectgrades[sectionnumber] = tempsect.shortGrade
            totG+=tempsect.shortGrade

        masterassnL = []

        for j in listofsections:
            for k in sectassn[j]:
                if not(k in masterassnL):
                    masterassnL.append(k)

        assnsectnumD = {}
        assncourseavgD = {}

        for m in masterassnL:
            assnsectnumL = []
            totalg = 0
            numsec = 0
            for n in listofsections:
                tsect = dictionary[n]
                if m in sectassn[n]:
                    assnsectnumL.append(n)
                    if not(type(tsect.agradeDict[m]) == list):
                        totalg += tsect.agradeDict[m]
                    numsec += 1
                assnsectnumD[m] = assnsectnumL
            if not(totalg == 0):
                assncourseavgD[m] = totalg/numsec

        self.avgG = totG/len(listofsections)
        self.snumsL = listofsections
        self.allstu = allstuL
        self.masterassnL = masterassnL
        self.sectD = dictionary
        self.sectusers = sectusers
        self.sectgrades = sectgrades
        self.assnsectnumD = assnsectnumD
        self.assncourseavgD = assncourseavgD

    def __str__(self):
        # This will eventually print useful information about the course
        rope = 'This is what comes out of print(course)'
        return rope


class section():
    """
    A class to represent a section.
    
    ...
    
    Attributes
    ----------
    snum : str
        Section number
    dataF : DataFrame
        all data for the section
    ptsD : dict
        key = assignment name, str and entry = points possible, float
    stuL : lst
        list of all student usernames, str, in the section
    assignL : lst
        list of all assignments, str, that have point values in the section
    assnDict : dict
        key = assignment name, str and entry = assignment, class object
    agradeDict : dict
        key = assignment name, str and entry = average section grade, float
    anosubDict : dict
        key = assignment name, str and entry = usernames, str, that have not submitted in lists
    aneedsgradeDict : dict
        key = assignment name, str and entry = usernames, str, that need grades in lists
    shortGrade : float
        average percentage without grades below 30% or high levels of nosub/needsgrade
    allGrade : float
        average percentage of all students
    stuDict : dict
        key = username, str and entry = student, class object
    snosubDict : dict
        key = username, str and entry = assignments, str, that need submission in lists
    sneedsgradeDict : dict
        key = username, str and entry = assignments, str, that need grading in lists
    """
    
    def __init__(self,sectionnum,filename):
        """
        Compiles and calculates all necessary information about the section object.
        
        Parameters
        ----------
        filename : str
            file name where the section data is located
        """
        dataF = pd.read_csv(filename)
        self.snum = sectionnum

        dropColumns = ['Availability', 'Weighted Total',
                       'Total [Total', 'Safety Contract']

        # Data Wrangling
        matching = [s for s in dataF.columns if any(
            xs in s for xs in dropColumns)]
        dataF = dataF.drop(columns=matching)
        ### ADD THIS IN AS AN OPTION BUT I WANT IT IN FOR NOW ###
        # Drop columns that received no submissions
        deadColumnsBool = dataF.isnull().values.all(axis=0)
        deadColumns = []
        for i in range(len(deadColumnsBool)):
            if deadColumnsBool[i] == True:
                ind = dataF.columns[i]
                deadColumns.append(ind)
        dataF = dataF.drop(columns=deadColumns)
        dataF = dataF[:].fillna('No Submission')

        collist = []
        pointsD = {}
        # assignL = []
        for k in dataF.columns:
            end = k.find(']')
            if 'Attendance' in k:
                collist.append('Attendance')
            elif 'Complete/Incomplete' in k:
                collist.append(k[0:start-2])
                # assignL.append(k[0:start-2]) #
            elif end != -1:
                start = k.find('[')
                start = k.find('[')
                pointsD[k[0:start-1]] = float(k[start+12:end-6])
                collist.append(k[0:start-1])
                # assignL.append(k[0:start-1])
            else:
                collist.append(k)
        dataF.columns = collist
        dataF = dataF.set_index(['Username'])

        self.dataF = dataF
        self.ptsD = pointsD
        stuL = dataF.index.values.tolist()
        self.stuL = stuL
        assignL = list(pointsD.keys())
        self.assignL = assignL

        # Create all assignment objects and store them in a dictionary
        adict = {}
        agradeD = {}
        anosubD = {}
        aneedsgradeD = {}
        for j in assignL:
            atemp = assignment(j, stuL, pointsD, dataF)
            adict[j] = atemp
            agradeD[j] = atemp.avgper
            if not(atemp.nosub == ['All assignments have been submitted']):
                anosubD[j] = atemp.nosub
            if not(atemp.needsgrade == ['No assignments need grading']):
                aneedsgradeD[j] = atemp.needsgrade

        self.assnDict = adict
        self.agradeDict = agradeD
        self.anosubDict = anosubD
        self.aneedsgradeDict = aneedsgradeD

        # Create all student objects and store them in a dictionary
        sdict = {}
        snosubD = {}
        sneedsgradeD = {}
        total = 0
        stuNum = 0
        alltotal = 0
        allstuNum = 0
        for m in stuL:
            stemp = student(m, pointsD, dataF)
            sdict[m] = stemp
            snosubD[m] = stemp.nosub
            sneedsgradeD[m] = stemp.needsgrade

            alltotal += stemp.shortPer
            allstuNum += 1

            if stemp.shortPer < 40 or ((len(stemp.nosub)+len(stemp.needsgrade))/len(list(stemp.gradesD.keys())) > 0.3):
                # ***If a student has stopped submitting work and received a ton of 0's***
                # ***or needs a significant amount submitted or graded don't include them***
                # ***in the section average. I chose the 40/0.3 based on observation.***
                continue
            else:
                total += stemp.shortPer
                stuNum += 1

        self.shortGrade = total/stuNum
        self.allGrade = alltotal/allstuNum
        self.stuDict = sdict
        self.snosubDict = snosubD
        self.sneedsgradeDict = sneedsgradeD
    def __str__(self):
        # This will eventually print useful information about the section
        bra = ['[',']']
        rope = ("""Section: {0} \n""" \
                """Average Section Grade: {1} \n""" \
                """------------------------ \n""" \
                """Average Assignment Grade \n""" \
                """------------------------ \n""" \
                """{2} \n""" \
                """------------------------ \n""" \
                """   Missing Submissions \n""" \
                """------------------------ \n""" \
                """{3} \n"""
                """------------------------ \n""" \
                """WOO \n""").format(self.snum,round(self.shortGrade,2),json.dumps(self.agradeDict,indent=1)[2:-2],json.dumps(self.anosubDict,indent=1).replace('[','').replace(']','').replace(',','')[2:-4])
        return rope