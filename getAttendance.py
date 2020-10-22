import pandas as pd
import re
from datetime import date

df = pd.read_csv('10182020.csv')
total = 0
noNumber = 0
withoutNumber = set()
original_names = []

# read through all names and clean them up
for x, row in df.iterrows():
    orig = str(row['Name (Original Name)'])

    # this regex finds the beginning name and then excludes the parenthesis and what is inside them
    name_check = re.search(r".*(?=\(.*\))", orig)
    if name_check is None:
        #original_names.append(orig.replace(" ", ""))
        original_names.append(orig.strip())
    else:
        #original_names.append(name_check[0].replace(" ", ""))
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
        total = total + int(attendee[0])
    else:
        print("no attendance number")
        noNumber += 1
        withoutNumber.add(name)

print('Number in attendance: ', total)
print('Number without attendance: ', noNumber)
print(withoutNumber)

file1 = open('report.txt', 'w')
today = date.today()

file1.write("Meeting Attendance for " + today.strftime("%m/%d/%Y") + "\n")
file1.write("Total attendance counted: " + str(total) + "\n")
file1.write("Total devices that couldn't be counted: " + str(noNumber) + "\n")
file1.write("Those needing contacted:\n")
file1.writelines('%s\n' % l for l in withoutNumber)
file1.close()
