## Boilerplate Code. Taken from DALAssembler.py

#Set this to true if we are debugging our code. It will override all command line arguments.
debug = True

#Convert an address into a big endian and little endian string
def findBELEcode(addr):
    if(addr[0] == '$'):
        addr = addr[1::]
    addr = "0x" + str(addr)
    addr = int(addr, 16)
    BE = addr >> 8
    LE = addr & 0xFF
    return (BE, LE)

def getReg(reg: str):
    if(reg == 'a'):
        return 0
    elif(reg == 'b'):
        return 1
    elif(reg == 'x'):
        return 2
    elif(reg == 'y'):
        return 3
    else:
        print("Invalid Register")
        return -1   

#Imports
import sys, binascii

#Every label must have one of these characters
requiredChars = ["g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

#Store our register names and their values
REGA = 0
REGB = 1
REGX = 2
REGY = 3

#Default output file name
outFile = "a.dml"

#Keep track of how many arguments we have found
argumentsFound = 0

#List of extensions we will output to
fileExtensions = [
    ".bin",
    ".txt",
    ".lst"
]

#File name
fileName = ""

#If we are not debugging, we will use this to process the command line arguments
if not debug:
    #Check if we have any arguments. If not, alert user that no file was given, and exit.
    if(len(sys.argv) == 1):
        print("No file specified")
        sys.exit(1)

    #Check all arguments supplied
    for argIndex in range(1, len(sys.argv)):
        #Check if the argument is the "output" argument
        if(sys.argv[argIndex] == "-o"):
            #Set the output file, and increment argument count by 2
            outFile = sys.argv[argIndex + 1]
            argumentsFound += 2
        #If the user asks for help, print the help message and exit
        elif(sys.argv[argIndex] == "-h"):
            print("""
    DAL Assembly Tool V2
            Usage: DALAssembler.py [-o <output file>] <input file>
            -o <output file> - Specify the output file.
            <input file> - Specify the input file.
            -h - Print this help message.
            
    Designed By: Alex Dasneves
    """)
            sys.exit(0)
    #If the user did not supply a valid output file
    if(not ".dal" in sys.argv[len(sys.argv) - 1]):
        print("Invalid file extension or no file specified!")
        sys.exit(1)
    #Set the file name
    fileName = sys.argv[len(sys.argv) - 1]
    #fileName = "testProgram.dal"
else:
    #If we are debugging, just set the output to be test.dal
    fileName = "test.dal"

#Current Lines from the file
inputLines = []

#All label locations and names
labels = []

#All jump instruction locations
linesToResolve = []

output = [0] * 65536

outputIndex = 0;

#Open the file
with open() as fileIn:
    for line in fileIn:
        inputLines.append(line.lower())

## Pass I: Resolve everything except for jump instructions.

for currentLine in inputLines:
    pass
    instruction = currentLine.split(" ")[0]
    if(instruction == "jmp"):
        linesToResolve.append([outputIndex, currentLine])
        outputIndex += 3
    elif(instruction == "bne"):
        linesToResolve.append([outputIndex, currentLine])
        outputIndex += 3
    elif(instruction == "beq"):
        linesToResolve.append([outputIndex, currentLine])
        outputIndex += 3
    elif(instruction == "jsr"):
        linesToResolve.append([outputIndex, currentLine])
        outputIndex += 3
    elif(instruction == "jse"):
        linesToResolve.append([outputIndex, currentLine])
        outputIndex += 3
    elif(instruction == "jsn"):
        linesToResolve.append([outputIndex, currentLine])
        outputIndex += 3
    elif(instruction == "nop"):
        output[outputIndex] = 0
        outputIndex += 1
    elif(instruction == "brk"):
        output[outputIndex] = 0xFF
        outputIndex += 1
    elif(instruction == "hlt"):
        output[outputIndex] = 0xF7
        outputIndex += 1
    elif(instruction == "ctn"):
        output[outputIndex] = 0xFE
        outputIndex += 1
    elif(instruction == "rst"):
        output[outputIndex] = 0xF9
        outputIndex += 1
    elif(instruction == "ret"):
        output[outputIndex] = 0x8C
        outputIndex += 1
    elif(instruction == "lsl"):
        output[outputIndex] = 0b01010100 | getReg(currentLine.split(" ")[1])
        outputIndex += 1
    elif(instruction == "lsr"):
        output[outputIndex] = 0b01010101 | getReg(currentLine.split(" ")[1])
        outputIndex += 1
    elif(instruction == "psh"):
        output[outputIndex] = 0xC1
        outputIndex += 1
        output[outputIndex] = getReg(currentLine.split(" ")[1]) << 6
        outputIndex += 1
    elif(instruction == "pop"):
        output[outputIndex] = 0xC2
        outputIndex += 1
        output[outputIndex] = getReg(currentLine.split(" ")[1]) << 6
        outputIndex += 1  
    elif(instruction[::1] == "LD"):
        pass
## Pass II: Resolve Label Locations


## Pass III: Resolve Jump Instructions


## Write files