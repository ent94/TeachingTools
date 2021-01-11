# Simple script to create website from the current folder

MODULENAME=TeachingTools

# Generate automatic documentation
pdoc3 --force --html --output-dir ./docs $MODULENAME 

# Convert project README.md as the website index.html page
python Readme2Index.py ./README.md > docs/index.html
