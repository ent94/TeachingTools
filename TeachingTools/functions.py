"""
Assign a letter grade to a percentage score.

...

Methods
-------
determine_grade(scores)
    Returns the letter grade for the given percentage score.
"""
def determine_grade(scores):
    """
    Return the letter grade for the given percentage score.
    Parameters
    ----------
    scores : float
        Percentage score to be converted
    Returns
    -------
    string : str
        Letter grade for the given score
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
