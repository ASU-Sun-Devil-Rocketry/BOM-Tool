### Commands.py -- module with all BOM command line functions 
### Author: Colton Acosta
### Date: 1/18/2021
### Sun Devil Rocketry Avionics

# Standard Imports
import sys

# exitFunc -- quits the program
def exitBOM():
   sys.exit()

# helpFunc -- displays list of commands
def helpFunc():
    print('BOM Tool Commands: \n')

# prodBOM -- creates production BOM
def prodBOM():
    print("Creating Production BOM ...")
    print("Production BOM successfully created")

# Command List
commands = { "exit": exitBOM,
             "production": prodBOM,
             "help": helpFunc
        }

# parseInput -- checks user input against command list 
#               options
# input: user inputed string
# output: none
def parseInput(userin): 

    # Get rid of any whitespace
    userin.strip()

    # Check if user input corresponds to a function
    for command in commands: 
        if userin == command:
           commands[command]()
           return None

    # User input doesn't correspond to a command
    print("Invalid BOM command")
    userin = input("BOM> ")
    parseInput(userin)

