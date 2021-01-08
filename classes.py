import pandas as pd
import os
from functions import determine_grade

class student():
    def __init__(self,username,ptsDict,sectDF):
        # I have been using the .str as a quick test plz ignore
        self.str = 'Hello World Student'
        
        # Initialize useful variables outside loop
        nosub = []
        needsgrade = []
        shortL = []
        gradesD = {}
        stuPts = 0
        shortPoss = 0
        longPoss = 0
        
        # Loop over assignment names
        for i in list(ptsDict.keys()):
            # Set the gtemp variable to the correct cell value in the data frame
            gtemp = sectDF.at[username,i]
            # Get the possible points from the dictionary
            possPts = ptsDict[i]
            # Add the possible points to the running total possible points including all assignments
            longPoss+=possPts
            if gtemp == 'No Submission':
                # If the gtemp value is 'No Submission', add the assignment name to the nosub list
                nosub.append(i)
            elif gtemp == 'Needs Grading':
                # If the gtemp value is 'Needs Grading', add the assignment name to the needsgrade list
                needsgrade.append(i)
            else:
                # This leaves only the graded assignments
                # Set gtemp to a float value because sometimes .csv imports number as string
                gtemp = float(gtemp)
                # Add the points the student earned to their running total
                stuPts+=gtemp
                # Add the points possible to the running total for graded assignments only
                shortPoss+=possPts
            # Add key = assignment name and entry = grade or 'No Submission' or 'Needs Grading' to dictionary
            gradesD[i] = gtemp
            
        if needsgrade == []:
            # If no assignemnts have been added to needsgrade add this message
            needsgrade.append('No assignments need grading')
        if nosub == []:
            # If no assignemnts have been added to nosub add this message
            nosub.append('All assignments have been submitted')
        
        # A dictionary with key = assignment name and entry = grade for that assignment
        self.gradesD = gradesD
        
        # A list of assignment names that 'Need Submission'
        self.nosub = nosub
        
        # A list of assignment names that 'Need Grading'
        self.needsgrade = needsgrade
        
        # Percentage grade for the student including all possible assignments
        allPer = (stuPts/longPoss)*100
        self.allPer = allPer
        
        # Letter grade for this
        self.allLet = determine_grade(allPer)
        
        # Percentage grade for the student excluding 'Needs Submission' and 'Needs Grading'
        shortPer = (stuPts/shortPoss)*100
        self.shortPer = shortPer
        
        # Letter grade for this
        self.shortLet = determine_grade(shortPer)
        
    def __str__(self):
        # This will eventually print useful information about the student
        rope = 'This is what comes out of print(student)'
        return rope

class assignment():
    def __init__(self,aname,stuL,ptsDict,sectData):
        # I have been using the .str as a quick test plz ignore
        self.str = 'Hello World Assignment'
        
        # Get the points possible for the assignment from the dictionary
        pts = ptsDict[aname]
        
        # Initialize useful variables outside loop
        needsgrade = []
        nosub = []
        nstu = 0
        tot = 0
        
        # Loop over student usernames
        for i in stuL:
            # Set the gtemp variable to the correct cell value in the data frame
            grade = sectData.at[i,aname]
            if grade == 'Needs Grading':
                # If the grades value is 'Needs Grading', add the assignment name to the needsGrade list
                needsgrade.append(i)
            elif grade == 'No Submission':
                # If the grade value is 'No Submission', add the assignment name to the noSub list
                nosub.append(i)
            elif float(grade) == 0:
                # If the grade value is 0, just skip onto the next student
                continue
            else:
                # increase the number of students included in the average by 1
                nstu+=1
                # increase the sum of all the grades by that student's grade
                tot+=float(grade)
                
        if pts == 0:
            # If pts is 0 then the assignment it extra credit, set the variables as such
            p = ['This is an extra credit assignment. No average score is needed']
            let = ['This is an extra credit assignment. No letter is given']
        else:
            # If pts != 0 then the assigment percentage should be the (average score/points possible)*100
            p = (tot/nstu)/pts*100
            let = determine_grade(p)
        if needsgrade == []:
            # If no assignemnts have been added to needsGrade add this message
            needsgrade.append('All submitted assignments have been graded')
        if nosub == []:
            # If no assignemnts have been added to noSub add this message
            nosub.append('All assignments have been submitted')
        
        # Percent grade for the assignment in the section without Needs Grading, No Submission, or 0's
        self.avgper = p
        
        # Letter grade for this
        self.avglet = let
        
        # A list of usernames with 'Needs Grading'
        self.needsgrade = needsgrade
        
        # A list of usernames with 'No Submission'
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
    
    def __init__(self,directory):
        # I have been using the .str as a quick test plz ignore
        self.str = 'Hello World Course'
        
        # Initialize useful variables outside loop
        dictionary = {}
        sectusers = {}
        sectassn = {}
        sectgrades = {}
        assngrades = {}
        listofsections = []
        allstuL = []
        totG = 0
        
        # Loop over files in the directory
        for i in sorted(os.listdir(directory)):
            # Set the sectionnumber to the correct portion of the file name
            sectionnumber = i[i.find('_')+1:len(i)-4]
            # Add the sectionnumber to the listofsections
            listofsections.append(sectionnumber)
            # Create a section object and store it as tempsect
            tempsect = section(os.path.join(directory, i))
            # Add key = sectionnumber and entry = section object to dictionary
            dictionary[sectionnumber] = tempsect
            # Add key = sectionnumber and entry = username list to dictionary
            sectusers[sectionnumber] = tempsect.stuL
            # Add usernames to master list
            allstuL.extend(tempsect.stuL)
            # Add key = sectionnumber and entry = assignment list to dictionary
            sectassn[sectionnumber] = tempsect.assignL
            # Add key = sectionnumber and entry = average student grade (short list)
            sectgrades[sectionnumber] = tempsect.shortGrade
            # Add the section grade to the total
            totG+=tempsect.shortGrade
        
        # Initialize useful variables outside loop
        masterassnL = []
        
        # Loop over section numbers
        for j in listofsections:
            # Loop over that list of assignmnet for that section
            for k in sectassn[j]:
                # Check to see if it is already in the masterlist
                if not(k in masterassnL):
                    # If it is not, add it to the list
                    masterassnL.append(k)
        
        # Initialize useful variables outside loop           
        assnsectnumD = {}
        assncourseavgD = {}
        
        # Loop over master list of assigments
        for m in masterassnL:
            # Initialize useful variables outside loop
            assnsectnumL = []
            totalg = 0
            numsec = 0
            # Loop over section numbers
            for n in listofsections:
                # Set tsect to the section object created above
                tsect = dictionary[n]
                # Check if the assignmentname m is in the assignments list for that section
                if m in sectassn[n]:
                    # If the assignment is in the list of assignments for that section
                    # Append the section number to a list
                    assnsectnumL.append(n)
                    # Check if the entry for the grade is a list (this means it's extra credit)
                    if not(type(tsect.agradeDict[m]) == list):
                        # Increase total g by the average score for that section
                        totalg+=tsect.agradeDict[m]
                    # Increase number of sections by 1
                    numsec+=1
                # Add key = assignmentname and entry = list of sections with that assignment to dictionary
                assnsectnumD[m] = assnsectnumL
            # Check to see if totalg is 0 (aka the assignment is extra credit)
            if not(totalg == 0):
                # If not Add key = assignmentname and entry = average course grade for that assignment
                assncourseavgD[m] = totalg/numsec

        # Average student grade in the course
        self.avgG = totG/len(listofsections)
        
        # A list of sectionnumbers as strings
        self.snumsL = listofsections
        
        # A list of all usernames in the course
        self.allstu = allstuL
        
        # A list of all assignments in the course
        self.masterassnL = masterassnL
            
        # A dictionary with key = sectionnumber and entry = section object to dictionary
        self.sectD = dictionary
        
        # A dictionary with key = sectionnumber and entry = list of users in that section
        self.sectusers = sectusers
        
        # A dictionary with key = sectionnumber and entry = average student grade
        self.sectgrades = sectgrades
        
        # A dictionary with key = assignmentname and entry = list of section numbers that contain that assignment
        self.assnsectnumD = assnsectnumD
        
        # A dictionary with key = assignmentname and entry = course average score
        self.assncourseavgD = assncourseavgD
        
    def __str__(self):
        # This will eventually print useful information about the course
        rope = 'This is what comes out of print(course)'
        return rope

class section():
    def __init__(self,filename):
        # I have been using the .str as a quick test plz ignore
        self.str = 'Hello World Section'
        
        # Read in the .csv file as a data frame
        dataF = pd.read_csv(filename)
        
        ### ***I haven't decided what to do with dropColumns...***
        # ***1. Should it just stay here?***
        # ***2. Should it be passed in as an input to create a section class?***
        # ***I vote 1. because it really only changes if this isn't Blackboard***
        # even then if it runs and doesn't identify the columns nothing happens but 'wasted computing time'
        dropColumns = ['Availability','Weighted Total','Total [Total','Safety Contract']
        
        # Data Wrangling
        
        # This gets rid of unwanted columns (from dropColumns list) in the data frame
        matching = [s for s in dataF.columns if any(xs in s for xs in dropColumns)]
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
        # Set na values to 'No Submission' because this makes work in student and assignment easier
        dataF = dataF[:].fillna('No Submission')
        
        # This loops over the column list to create:
        # 1. Shortened column headers like 'L2 - Worksheet'
        # 2. A dictionary with key = assignment name and entry = points possible
        collist = []
        pointsD = {}
        # assignL = [] # This would be useful for honors stuff but I don't need it right now
        for k in dataF.columns:
            end = k.find(']')
            if 'Attendance' in k:
                collist.append('Attendance')
            elif 'Complete/Incomplete' in k:
                collist.append(k[0:start-2])
                # assignL.append(k[0:start-2]) # This would be useful for honors stuff but I don't need it right now
            elif end != -1:
                start = k.find('[')
                start = k.find('[')
                pointsD[k[0:start-1]] = float(k[start+12:end-6])
                collist.append(k[0:start-1])
                # assignL.append(k[0:start-1]) # This would be useful for honors stuff but I don't need it right now
            else:
                collist.append(k)
        dataF.columns=collist
        
        # Set the index to the column called Username
        dataF = dataF.set_index(['Username'])
        
        
        # A data frame of all of the section data
        self.dataF = dataF
        
        # A dictionary with key = assignment name and entry = points possible
        self.ptsD = pointsD
        
        # A list of all student usernames in this section
        stuL = dataF.index.values.tolist()
        self.stuL = stuL
        
        # A list of all assignment names that have point values in this section (aka not honors work)
        assignL = list(pointsD.keys())
        self.assignL = assignL
        
        # Create all assignment objects and store them in a dictionary to be accessed
        adict = {}
        agradeD = {}
        anosubD = {}
        aneedsgradeD = {}
        for j in assignL:
            # Create an assignment object from the assignment name
            atemp = assignment(j,stuL,pointsD,dataF)
            # Add key = assignment name and entry = assignmentobject from that assignment name to dictionary
            adict[j] = atemp
            # Add key = assignment name and entry = average assignment grade to dictionary
            agradeD[j] = atemp.avgper
            # Add key = assignment name and entry = usernames that need submission to dictionary
            anosubD[j] = atemp.nosub
            # Add key = assignment name and entry = usernames that need grading to dictionary
            aneedsgradeD[j] = atemp.needsgrade
            
        # A dictionary with key = assignment name and entry = assignmentobject from that name
        self.assnDict = adict
        # A dictionary with key = assignment name and entry = avg grade for that assignment at section level
        self.agradeDict = agradeD
        # A dictionary with key = assignment name and entry = usernames that need submision
        self.anosubDict = anosubD
        # A dictionary with key = assignment name and entry = usernames that need grading
        self.aneedsgradeDict = aneedsgradeD
        
        # Create all student objects and store them in a dictionary to be accessed
        sdict = {}
        snosubD = {}
        sneedsgradeD = {}
        total = 0
        stuNum = 0
        alltotal = 0
        allstuNum = 0
        for m in stuL:
            # Create a student object for each username
            stemp = student(m,pointsD,dataF)
            # Add key = username and entry = studentobject from that username to dictionary
            sdict[m] = stemp
            # Add key = username and entry = list of assignment names that needs submission
            snosubD[m] = stemp.nosub
            # Add key = username and entry = list of assignment names that need grading
            sneedsgradeD[m] = stemp.needsgrade
            
            alltotal+=stemp.shortPer
            allstuNum+=1
            
            if stemp.shortPer < 40 or ((len(stemp.nosub)+len(stemp.needsgrade))/len(list(stemp.gradesD.keys()))>0.3):
                # If a student has stopped submitting work and received a ton of 0's or needs a significant amount submitted or graded don't include them in the section average
                # I chose the 40/0.3 based on observation of my students
                continue
            else:
                # Increase avgerageGrade and stuNum
                total+=stemp.shortPer
                stuNum+=1
        
        # Average percentage without below 30% grades and high numbers of no sub/needs grade
        self.shortGrade = total/stuNum
        
        # Average percentage of al students in the section
        self.allGrade = alltotal/allstuNum
        
        # A dictionary with key = username and entry = studentobject from that username
        self.stuDict = sdict
        
        # A dictionary with key = username and entry = list of assignment names that needs submission
        self.snosubDict = snosubD
        
        # A dictionary with key = username and entry = list of assignment names that need grading
        self.sneedsgradeDict = sneedsgradeD
        
        
    def __str__(self):
        # This will eventually print useful information about the section
        rope = 'This is what comes out of print(section)'
        return rope