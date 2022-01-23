### Commands.py -- module with all BOM command line functions 
### Author: Colton Acosta
### Date: 1/18/2021
### Sun Devil Rocketry Avionics

# Standard Imports
import sys
from datetime import date
import time

# JSON Formatting Imports
import jsonData
json = jsonData.jsonData()

## Production BOM Basic Data

# Convert Numbers to Letters
ExcelCols = ['Null', 'A','B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']

# Table Headers
prodBomHead = ['Item No.', 'Designator', 'Qty','Manufacturer', 'Mfg Part No.', 
                'Description/Value', 'Package/Footprint', 'Type', 'Notes']
designBomHead = ['Qty', 'Component', 'Manufacturer', 'Part Number', 'Designator', 
                 'Footprint', 'Footprint Type']

# Number of header rows 
prodBomHeadRows = 7

# exitFunc -- quits the program
def exitBOM(bom, Args):
   sys.exit()

# helpFunc -- displays list of commands
def helpFunc(bom, Args):
    print('BOM Tool Commands: \n')

# genBomHeader -- Generates the production bom header 
#                 format
# input: bom spreadsheet object
def genBomHeader(bom):
    designBom = bom.get_worksheet(0)
    prodBom = bom.get_worksheet(1)

    # Generate Header
    prodBom.merge_cells("A1:I2")
    prodBom.merge_cells("B3:I6", 'MERGE_ROWS')
    prodBom.update("A7:I7", [prodBomHead])
    title = designBom.acell("A1").value.split()
    title.insert(-1, "Production")
    title = ' '.join(title)
    prodBom.update("A1", title)
    prodBom.format("A1", {"textFormat": {"bold": True,
                          "fontSize": 18}})
    designHeadData = designBom.batch_get(["A3:B6"])
    prodBom.update("A3:B6", designHeadData[0])
    today = date.today().strftime("%m/%d/%Y")
    prodBom.update("B5", today)
    prodBom.format("A1:I7", json.borders)
    prodBom.format("A1:I6", json.lightColor)
    prodBom.format("A7:I7", json.darkColor)


# newProdBom -- creates new production bom
# input: bom spreadsheet object
def genProdBom(bom):

   # Open BOM Sheets
   designBom = bom.get_worksheet(0)
   prodBom = bom.get_worksheet(1)

   ## Loop over components and add data

   # Pull headers to determine target column numbers
   designHeaders = designBom.row_values(prodBomHeadRows)

   # Assign Each header a column number
   designHeaderMap = [4, 0, 2, 3, 1, 5, 6]
   baseDesignRow = 8
   designNumParts = len(designBom.col_values(1)) -8
   designTableA = ['A8:G'+str(len(designBom.col_values(1)))]
   partData = designBom.batch_get(designTableA)[0]
   prodPartData = []
   for row in partData:
       if len(row) == 7:
          prodPartData.append(list(row))
          for count, col in enumerate(designHeaderMap):
              prodPartData[-1][count] = row[col]

   # Write Data from lists to spreadsheet
   prodTableA = 'B8:H'+str(baseDesignRow+len(prodPartData))
   prodBom.update(prodTableA, prodPartData)
   itemNos = [*range(1, len(prodPartData)+1)] 
   itemNosV = [[x] for x in itemNos]
   prodFinalRow = baseDesignRow+len(prodPartData)-1
   itemNosTableA = 'A8:A'+str(prodFinalRow)
   prodBom.update(itemNosTableA, itemNosV)
   prodBom.format(itemNosTableA, {"horizontalAlignment": "LEFT"})
   
   # Add background color
   prodPartDataTableA = 'A8:I'+str(prodFinalRow)
   prodBom.format(prodPartDataTableA, json.borders)
   prodPartsTableA = 'A8:I'+str(prodFinalRow)
   prodBom.format(prodPartsTableA, json.lightColor)

   # Make every other row dark
   row = 9 
   while row <= prodFinalRow:
       prodRowTablesA = 'A'+str(row)+':I'+str(row)
       row+=2
       prodBom.format(prodRowTablesA, json.darkColor)

   # Write Marker Data to random cell to indicate bom 
   # was auto-generated
   prodBom.update("T100", "AUTO-GENERATED")

   # exit
   return(None)


# editProdBom -- updates production BOM to 
#                reflect recent changes to 
#                BOM
def editProdBom(bom):

    # production bom sheet
    designBom = bom.get_worksheet(0)
    prodBom = bom.get_worksheet(1)

    # Update date of generation
    today = date.today().strftime("%m/%d/%Y")
    prodBom.update("B5", today)

    # Delete Extra BOM entries
    prodBomSheetSize = len(designBom.col_values(1))
    prodBom.batch_clear(["A"+str(prodBomSheetSize)+":I100"])
    prodBom.format("A"+str(prodBomSheetSize)+":I100", json.defaultFormat)

    # Generate Production BOM Data
    genProdBom(bom)

# prodBOM -- creates production BOM
# input: bom spreadsheet object
def prodBOM(bom, Args):
    print("Creating Production BOM ...")

    # Read BOM headers to check BOM format is correct
    designBom = bom.get_worksheet(0)
    designBomHeaders = designBom.row_values(7)
    for headNo, head in enumerate(designBomHead):
        if head != designBomHeaders[headNo]:
            print('Error encountered while parsing BOM headers. The header "'  \
                    + designBomHead[headNo] + '" is not a proper header or is' \
                    'in the wrong position. The headers should be ordered: ')
            print()
            for itemNo, item in enumerate(designBomHead, 1):
                print("\t" + str(itemNo) + ". " + item)
            print()
            return None

    # Check if production BOM exists and/or
    # create new sheet
    # New sheet --> Generate new template 
    #             - Add data to header
    # Existing sheet --> Update new fields
    numsheets = len(bom.worksheets())
    if (numsheets == 1): # New Production BOM

        # create the new sheet
        bom.add_worksheet(title="Production BOM", rows="100", cols="20") 

        # Generate the header
        genBomHeader(bom)

        # Generate the BOM
        genProdBom(bom)

    elif(numsheets == 2): # Existing Production BOM

        # Check if BOM was auto generated, and ask user
        # if they'd like to overwrite the bom
        prodBom = bom.get_worksheet(1)
        autoMarker = prodBom.acell("T100").value
        if(autoMarker == "AUTO-GENERATED"):
            # Ask if user wants to overwrite the bom
            userChoice = input("""A Production BOM has already been generated. Would you like to update the current BOM? [y/n]:""")
            if(userChoice == "y" or userChoice == "Y"):
                editProdBom(bom)

            elif(userChoice == "n" or userChoice == "N"):
                print("Aborting operation...")
                return None
            else: 
                print("Invalid option. Aborting operation...")
                return None
        else:
            userChoice = input("The production BOM sheet contains data not generated by the BOM tool. Would you like to overwrite this data? [y/n]:")
            if(userChoice == "y" or userChoice == "Y"):
                bom.del_worksheet(prodBom)
                bom.add_worksheet(title="Production BOM", rows="100", cols="20")
                genBomHeader(bom)
                genProdBom(bom)
            elif(userChoice == "n" or userChoice == "N"):
                print("Aborting operation...")
                return None
            else: 
                print("Invalid option. Aborting operation...")

    else: # too many sheets
        print("Error: Too many BOM sheets. Check that there are no extra sheets in the BOM.")

    print("Production BOM successfully created")

# Command List
commands = { "exit": exitBOM,
             "production": prodBOM,
             "help": helpFunc
        }

# parseInput -- checks user input against command list 
#               options
# input: userin: user inputed string
#        bom: spreadsheet object
# output: none
def parseInput(userin, bom): 

    # Get rid of any whitespace
    userin.strip()

    # Split the input into commands and arguments
    userinSplit = userin.split() 
    userCommand = userinSplit[0]
    CommandArgs = userinSplit[1:] 

    # Check if user input corresponds to a function
    for command in commands: 
        if userCommand == command:
           commands[command](bom, CommandArgs)
           return None

    # User input doesn't correspond to a command
    print("Invalid BOM command")
    userin = input("BOM> ")
    parseInput(userin, bom)

### END OF FILE
