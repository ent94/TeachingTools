from TeachingTools import course 

def test_determine_grade():
    assert course.determine_grade(76.4) == 'C'
