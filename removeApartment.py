#Program to remove rows that are not single family homes
import csv

def hasNumbers(inputString):
  return any(char.isdigit() for char in inputString)

fo = open('SanJoseAptUnitRemoved.csv', 'w')
with open("SanJose_hazard_cgs.csv", "r") as f:
  reader = csv.reader(f)
  for i, line in enumerate(reader):
    if " STE " in line[2]:
       continue
    if " APT " in line[2]:
       continue
    if " HWY" in line[2]:
       continue
    if " UNIT " in line[2]:
       continue
    if "#" in line[2]:
       continue
    if "" == line[2]:
       continue
    if not hasNumbers(line[2]):
       continue
    fo.write(",".join(line)+'\n')
fo.close()
