### BOM Tool -- Python API tool to manage Sun Devil Rocketry 
###             PCB BOMs

from pprint import pprint

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
        pprint(self.pcbs)


         

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

# Display PCB Menu
