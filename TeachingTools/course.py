"""
Calculate, Organize, and Display useful information when teaching a course with multiple sections.

View information about individual students, assignments, and sections as well as overall course
 informtion across all sections.

...

Classes
-------
student()
    calculate and display information about an individual student
assignment()
    calculate and display information about an individual assignment
course()
    load in all data and compile/display course wide information
section()
    calculate and display information about an individual section

Methods
-------
determine_grade(scores)
    returns the letter grade for the given percentage score.
"""
import os
import json
import pandas as pd


def determine_grade(scores):
    """
    Return the letter grade for the given percentage score.
    Parameters
    ----------
    scores : float
        percentage score to be converted
    Returns
    -------
    string : str
        letter grade for the given score
    """
    if 93 <= scores <= 100:
        return 'A'
    if 90 <= scores < 93:
        return 'A-'
    if 87 <= scores < 90:
        return 'B+'
    if 83 <= scores < 87:
        return 'B'
    if 80 <= scores < 83:
        return 'B-'
    if 77 <= scores < 80:
        return 'C+'
    if 73 <= scores < 77:
        return 'C'
    if 70 <= scores < 73:
        return 'C-'
    if 67 <= scores < 70:
        return 'D+'
    if 63 <= scores < 67:
        return 'D'
    if 60 <= scores < 63:
        return 'D-'
    return 'F'


class student():
    """
    A class to represent a student.

    ...

    Attributes
    ----------
    uname : str
        student username
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
        """Print useful information about each student object."""
        newDict = {'noSub': json.dumps(self.nosub, indent=1)[2:-3],
                   'noGrade': json.dumps(self.needsgrade, indent=1)[2:-3]}

        for i in newDict.keys():
            newDict[i] = newDict[i].replace('[', '')
            newDict[i] = newDict[i].replace(']', '')
            newDict[i] = newDict[i].replace('"', '')
            newDict[i] = newDict[i].replace(',', '')

        rope = ("""Student Username: {0} \n"""
                """Average Score: {1} \n"""
                """Letter Grade: {2} \n"""
                """------------------------ \n"""
                """   Missing Submission \n"""
                """------------------------ \n"""
                """{3} \n"""
                """------------------------ \n"""
                """      Needs Grading \n"""
                """------------------------ \n"""
                """{4} \n""").format(self.uname,
                                     round(self.shortPer, 2),
                                     self.shortLet,
                                     newDict['noSub'],
                                     newDict['noGrade'])
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
            p = ['No average score']
            let = ['No letter grade']
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
        """Print useful information about each assignment object."""
        newDict = {'noSub': json.dumps(self.nosub, indent=1)[2:-3],
                   'noGrade': json.dumps(self.needsgrade, indent=1)[2:-3]}

        for i in newDict.keys():
            newDict[i] = newDict[i].replace('[', '')
            newDict[i] = newDict[i].replace(']', '')
            newDict[i] = newDict[i].replace('"', '')
            newDict[i] = newDict[i].replace(',', '')

        rope = ("""Assignment Name: {0} \n"""
                """Average Score: {1} \n"""
                """------------------------ \n"""
                """   Missing Submission \n"""
                """------------------------ \n"""
                """{2} \n"""
                """------------------------ \n"""
                """      Needs Grading \n"""
                """------------------------ \n"""
                """{3} \n""").format(self.aname,
                                     round(self.avgper, 2),
                                     newDict['noSub'],
                                     newDict['noGrade'])
        return rope


class course():
    """
    A class to represent an entire course.

    ...

    Attributes
    ----------
    cname : str
        course name
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
        key = assignmnet name, str and entry = section numbers, str, that have that
         assignment in lists
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
        if not(os.path.isdir(directory)):
            raise ValueError(
                "This is not a valid directory. Please check the path and try again.")

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
            tempsect = section(sectionnumber, os.path.join(directory, i))
            dictionary[sectionnumber] = tempsect
            sectusers[sectionnumber] = tempsect.stuL
            allstuL.extend(tempsect.stuL)
            sectassn[sectionnumber] = tempsect.assignL
            sectgrades[sectionnumber] = tempsect.shortGrade
            totG += tempsect.shortGrade

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
        """Print useful information about each course object."""
        newDict = {'avgSectGrade': json.dumps(self.sectgrades, indent=1)[2:-2],
                   'avgAssnGrade': json.dumps(self.assncourseavgD, indent=1)[2:-4]}

        for i in newDict.keys():
            newDict[i] = newDict[i].replace('[', '')
            newDict[i] = newDict[i].replace(']', '')
            newDict[i] = newDict[i].replace('"', '')
            newDict[i] = newDict[i].replace(',', '')

        rope = ("""Course: {0} \n"""
                """Average Course Score: {1} \n"""
                """------------------------ \n"""
                """ Average Section Score \n"""
                """------------------------ \n"""
                """{2} \n"""
                """------------------------ \n"""
                """Average Assignment Score \n"""
                """------------------------ \n"""
                """{3} \n""").format(self.cname,
                                     round(self.avgG, 2),
                                     newDict['avgSectGrade'],
                                     newDict['avgAssnGrade'])
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
    stud_nosub_dictict : dict
        key = username, str and entry = assignments, str, that need submission in lists
    sneedsgradeDict : dict
        key = username, str and entry = assignments, str, that need grading in lists
    """

    def __init__(self, sectionnum, filename):
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
            if not(atemp.needsgrade == ['All submitted assignments have been graded']):
                aneedsgradeD[j] = atemp.needsgrade

        self.assnDict = adict
        self.agradeDict = agradeD
        self.anosubDict = anosubD
        self.aneedsgradeDict = aneedsgradeD

        # Create all student objects and store them in a dictionary
        sdict = {}
        stud_nosub_dict = {}
        sneedsgradeD = {}
        total = 0
        stuNum = 0
        alltotal = 0
        allstuNum = 0
        for m in stuL:
            stemp = student(m, pointsD, dataF)
            sdict[m] = stemp
            stud_nosub_dict[m] = stemp.nosub
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
        self.stud_nosub_dictict = stud_nosub_dict
        self.sneedsgradeDict = sneedsgradeD

    def __str__(self):
        """Print useful information about each section object."""
        newDict = {'avgAssnGrade': json.dumps(self.agradeDict, indent=1)[2:-2],
                   'noSub': json.dumps(self.anosubDict, indent=1)[2:-4],
                   'noGrade': json.dumps(self.aneedsgradeDict, indent=1)[2:-4]}

        for i in newDict.keys():
            newDict[i] = newDict[i].replace('[', '')
            newDict[i] = newDict[i].replace(']', '')
            newDict[i] = newDict[i].replace('"', '')
            newDict[i] = newDict[i].replace(',', '')

        rope = ("""Section: {0} \n"""
                """Average Section Score: {1} \n"""
                """------------------------ \n"""
                """   Missing Submission \n"""
                """------------------------ \n"""
                """{2} \n"""
                """------------------------ \n"""
                """      Needs Grading \n"""
                """------------------------ \n"""
                """{3} \n"""
                """------------------------ \n"""
                """Average Assignment Score \n"""
                """------------------------ \n"""
                """{4} \n""").format(self.snum,
                                     round(self.shortGrade, 2),
                                     newDict['noSub'],
                                     newDict['noGrade'],
                                     newDict['avgAssnGrade'])
        return rope
