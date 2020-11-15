import pandas as pd
import re
import sys
from datetime import date
from datetime import timedelta
from emails import *
from weekend import *

file_name = sys.argv[1]
df = pd.read_csv(file_name)
total = 0
noNumber = 0
withoutNumber = set()
original_names = []

# get date information
today = date.today()
weekend = the_weekend()
the_date = today - timedelta(days=1) if weekend == 0 else today

# read through all names and clean them up
for x, row in df.iterrows():
    orig = str(row['Name (Original Name)'])

    # this regex finds the beginning name and then excludes the parenthesis and what is inside them
    name_check = re.search(r".*(?=\(.*\))", orig)
    if name_check is None:
        # original_names.append(orig.replace(" ", ""))
        original_names.append(orig.strip())
    else:
        # original_names.append(name_check[0].replace(" ", ""))
        original_names.append(name_check[0].strip())

# regex captures (*) but then negates: \b(?:(?!\(.*\)))\b
# this captures all (name): \(.*\)
# this selects all text but not (name): .*(?=\(.*\))
print(original_names)
print(len(original_names))
removed_duplicates = list(dict.fromkeys(original_names))
print(removed_duplicates)
print(len(removed_duplicates))

for name in removed_duplicates:
    attendee = re.search(r"\d", name)
    print(name)
    if attendee:
        print(attendee[0])
        total += int(attendee[0])
    else:
        print("no attendance number")
        noNumber += 1
        withoutNumber.add(name)

print('Number in attendance: ', total)
print('Number without attendance: ', noNumber)
print(withoutNumber)

with open('report.txt', 'w') as file1:
    file1.write("Meeting Attendance for " + the_date.strftime("%m/%d/%Y") + "\n")
    file1.write("Total attendance counted: " + str(total) + "\n")
    file1.write("Total devices that couldn't be counted: " + str(noNumber) + "\n")
    file1.write("Those needing contacted:\n")
    file1.writelines('%s\n' % l for l in withoutNumber)
send_email(weekend, the_date.strftime("%m/%d/%Y"))
