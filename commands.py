### Commands.py -- module with all BOM command line functions 
### Author: Colton Acosta
### Date: 1/18/2021
### Sun Devil Rocketry Avionics

# Standard Imports
import sys
from datetime import date

## Production BOM Basic Data

# Table Headers
prodBomHead = ['Item No.', 'Designator', 'Qty', 'Mfg Part No.', 
                'Description/Value', 'Package/Footprint', 'Type', 'Notes']
# Number of header columns
prodBomHeadCols = 7
# Header Formats
lightColor = {
                 "backgroundColorStyle": {
                    "rgbColor": {
                        "red": 256 - 239,
                        "green": 256 - 239,
                        "blue": 256 - 239,
                     }
                  }
               }
darkColor = {
                "backgroundColorStyle": {
                    "rgbColor": {
                        "red": 256 - 204,
                        "green": 256 - 204,
                        "blue": 256 - 204
                     }
                  }
             }


# exitFunc -- quits the program
def exitBOM(bom):
   sys.exit()

# helpFunc -- displays list of commands
def helpFunc(bom):
    print('BOM Tool Commands: \n')

# newProdBom -- creates new production bom
# input: bom spreadsheet object
def newProdBom(bom):

   # Design BOM
   designBom = bom.sheet1

   # create the new sheet
   prodBom = bom.add_worksheet(title="Production BOM", rows="100", cols="20") 

   # Generate Header
   prodBom.merge_cells("A1:H2")
   prodBom.merge_cells("B3:H6", 'MERGE_ROWS')
   for count,header in enumerate(prodBomHead, 1):
       prodBom.update_cell(prodBomHeadCols, count, header)
   title = designBom.acell("A1").value.split()
   title.insert(-1, "Production")
   title = ' '.join(title)
   prodBom.update("A1", title)
   prodBom.format("A1", {"textFormat": {"bold": True,
                         "fontSize": 18}})
   prodBom.update("A3", "Project: ")
   project = designBom.acell("B3").value
   prodBom.update("B3", project)
   prodBom.update("A4", "Revision: ")
   rev = designBom.acell("B4").value
   prodBom.update("B4", rev)
   prodBom.update("A5", "Date: ")
   today = date.today().strftime("%m/%d/%Y")
   prodBom.update("B5", today)
   prodBom.update("A6", "Author:  ")
   author = designBom.acell("B6").value
   prodBom.update("B6", author)
   prodBom.format("A1:H7", {
                              "borders": {
                                  "top": {
                                      "style": "SOLID"
                                  },
                                  "bottom": {
                                      "style": "SOLID"
                                  },
                                  "left": {
                                      "style": "SOLID"
                                  },
                                  "right": {
                                      "style": "SOLID"
                                  }
                              } 
                           })
   prodBom.format("A1:H6", lightColor)
   prodBom.format("A7:H7", darkColor)

   # Loop over components and add data
    
   
   # exit
   return(None)


# editProdBom -- updates production BOM to 
#                reflect recent changes to 
#                BOM
def editProdBom(bom):
    return None

# prodBOM -- creates production BOM
# input: bom spreadsheet object
def prodBOM(bom):
    print("Creating Production BOM ...")

    # Check if production BOM exists and/or
    # create new sheet
    # New sheet --> Generate new template 
    #             - Add data to header
    # Existing sheet --> Update new fields
    numsheets = len(bom.worksheets())
    if (numsheets == 1): # New Production BOM
        newProdBom(bom)
    elif(numsheets == 2): # Existing Production BOM
        editProdBom(bom)
    else: # too many sheets
        print("""Error: Too many BOM sheets. Check that
                there are no extra sheets in the BOM.""")

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

    # Check if user input corresponds to a function
    for command in commands: 
        if userin == command:
           commands[command](bom)
           return None

    # User input doesn't correspond to a command
    print("Invalid BOM command")
    userin = input("BOM> ")
    parseInput(userin, bom)

