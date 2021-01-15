from TeachingTools import course 
import pytest

def test_course_good():
    data = course.course('./exampledata/CEM153/')
    assert type(data.sectgrades) == dict
    
def test_course_bad():
    with pytest.raises(ValueError) as excinfo:
        course.course('./junk.txt')
    assert "This is not a valid directory" in str(excinfo.value)
