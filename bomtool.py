### BOM Tool -- Python API tool to manage Sun Devil Rocketry 
###             PCB BOMs

# Google Sheets API includes
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

# Standard imports
import sys

# Custom modules
import commands

# PCB class -- contains PCB information extracted from pcbs.txt
class pcb: 

    # Initializer- pcbdata contains source 
    #              file name
    def __init__(self, pcbdata): 
       
        # Extract line data from txt file
        self.file = pcbdata
        with open(self.file) as sourcefile:
            lines = sourcefile.readlines()

        # Initialize Dictionary for PCB data
        self.pcbs = {}

        # Parse Data:
        for line in lines: 
           # Check if line starts with "h" for "https" 
           if(line[0] == 'h'):
               self.pcbs[self.pcbnum].append(line)
           else: 
               self.pcbnum = line[0:5]
               self.pcbs[self.pcbnum] = [line[6:-1]]

        # Determine Number of PCBs
        self.numpcbs = len(self.pcbs)

# getOption -- Recursively ask the user for a new selection
#              until a valid option is entered
# Inputs: 
#         choice -- previous selection
#         options -- number of valid options
# Output:
#         choice -- Valid selection
def getOption(choice, options):

    # User enters a number
    try:     
        choice = int(choice)
        if (choice >= 1 and choice <= options):
            return(choice)
        else: 
            choice = input('Invalid selection. Try again: ')
            getOption(choice, options)
    # User enters a non-number
    except ValueError:
        choice = input('Invalid selection. Try again: ')
        getOption(choice, options)


### CODE START ### 

# Load PCBs from txt file
pcbs = pcb("pcbs.txt")
pcbtable = []
print('Loading PCBs...\n')

# Display PCB Menu
print('Choose a PCB: ')
for count,board in enumerate(pcbs.pcbs, 1):
    print('\t{}. {} - {}'.format(count, board, pcbs.pcbs[board][0]))
    pcbtable.append(board)

# Get User Choice
pcbChoice = input("Selection: ")
pcbChoice = getOption(pcbChoice, pcbs.numpcbs) 
pcbChoiceNum = pcbtable[pcbChoice-1] 

# Get User choice of revision number
rev = input("Enter the PCB revision: ")
numrevs = len(pcbs.pcbs[pcbChoiceNum]) -1
rev = getOption(rev, numrevs)

# Load the spreadsheet
url = pcbs.pcbs[pcbChoiceNum][rev]
gsheet_creds = ServiceAccountCredentials.from_json_keyfile_name("credentials-sheets.json", scope)
gsheet_client = gspread.authorize(gsheet_creds)
print('loading BOM spreadsheet...')
bom = gsheet_client.open_by_url(url).sheet1
print('BOM successfully loaded into program')

# Enter program loop
while(True):

   # Command prompt: 
   userin = input("BOM> ")
  
   # Parse respond to user input
   commands.parseInput(userin)

### PROGRAM END
