# Assembled from source found on various sites
# C Kohl Jan 2020
#
# Read in CSV File and reformat date-time value for importing properly to Salesforce
#
# Specify Input Filename.   Output filename is dervied from it.
#
#

# importing csv module
import csv

# INPUT CSV FILENAME <<<<<<<<<<   Can turn this into a parameter passed in
InputFilename  = "Vol Hours Upload 2 Jan 2020.csv"

# Output Filename Derived from Input Name
OutputFilename = InputFilename.replace(".csv"," - For Import.csv")

# initializing the titles and rows list
fields = []
rows = []

# reading csv file
with open(InputFilename, 'r') as csvfile:
    # creating a csv reader object
    csvreader = csv.reader(csvfile)

    # extracting field names through first row
#    FOR 3.7 .next()  FOR 3.8   __next__()
    fields = csvreader.__next__()
#    fields = csvreader.next()  


    # extracting each data row one by one
    for row in csvreader:
        rows.append(row)

    # get total number of rows
    print("Total no. of rows: %d" % (csvreader.line_num))

# printing the field names
# print('Field names are:' + ', '.join(field for field in fields))

# printing first 5 rows
# print('\nFirst 5 rows are:\n')
# for row in rows[:5]:

# processing all rows - admittedly brute force method.  Could be more elegant!
# must turn time to 24-hour format, remove AM PM, insert T between date and time
# finally must switch date to yyyy-mm-dd
#
for row in rows:
    # parsing each column of a row
#    for col in row:
#        print("%10s \n" % col),
#   print(row[0],row[11])
    stdttm=row[11]
    if "PM" in stdttm:
#	print('A PM Time was found')
        stdttm=stdttm.replace(" 01:"," 13:")
        stdttm=stdttm.replace(" 02:"," 14:")
        stdttm=stdttm.replace(" 03:"," 15:")
        stdttm=stdttm.replace(" 04:"," 16:")
        stdttm=stdttm.replace(" 05:"," 17:")
        stdttm=stdttm.replace(" 06:"," 18:")
        stdttm=stdttm.replace(" 07:"," 19:")
        stdttm=stdttm.replace(" 08:"," 20:")
        stdttm=stdttm.replace(" 09:"," 21:")
        stdttm=stdttm.replace(" 10:"," 22:")
        stdttm=stdttm.replace(" 11:"," 23:")
    stdttm=stdttm.replace(" AM",":00")
    stdttm=stdttm.replace(" PM",":00")
    stdttm=stdttm.replace(" ", "T")
    stdttm=stdttm[6:10]+'-'+stdttm[0:2]+'-'+stdttm[3:5]+stdttm[10:]




    row[11]=stdttm
#    print('\n')
#    date=stdttm[0:10]
#    print(date)
#    print('\n')

# writing to csv file
with open(OutputFilename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(rows)

