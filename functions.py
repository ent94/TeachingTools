def determine_grade(scores):
    if scores >= 93 and scores <= 100:
        return 'A'
    elif scores >= 90 and scores < 93:
        return 'A-'
    elif scores >= 87 and scores < 90:
        return 'B+'
    elif scores >= 83 and scores < 87:
        return 'B'
    elif scores >= 80 and scores < 83:
        return 'B-'
    elif scores >= 77 and scores < 80:
        return 'C+'
    elif scores >= 73 and scores < 77:
        return 'C'
    elif scores >= 70 and scores < 73:
        return 'C-'
    elif scores >= 67 and scores < 70:
        return 'D+'
    elif scores >= 63 and scores < 67:
        return 'D'
    elif scores >= 60 and scores < 63:
        return 'D-'
    else:
        return 'F'

def meancalc(lst):
    nstu = 0
    tot = 0
    for i in lst:
        if i == 'Needs Grading':
            continue
        elif i == 'No Submission':
            continue
        else:
            nstu+=1
            tot+=float(i)
    return tot/nstu