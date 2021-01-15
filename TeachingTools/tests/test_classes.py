from TeachingTools import classes
import pytest

def test_course_good():
    data = classes.course('./exampledata/CEM153/')
    assert type(data.sectgrades) == dict
    
def test_course_bad():
    with pytest.raises(ValueError) as excinfo:
        classes.course('./junk.txt')
    assert "This is not a valid directory" in str(excinfo.value)