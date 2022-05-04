import sys
if sys.version_info[0] > 3:
    raise Exception("Must be using Python 3")

debug = True


def findAddr(addr: str):
    if(addr[0] == '$'):
        addr = addr[1::]
    addr = "0x" + str(addr)
    addr = int(addr, 16)
    BE = addr >> 8
    LE = addr & 0xFF
    return (BE, LE)

requiredChars = ["g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]


REGA = 0
REGB = 0
REGX = 0
REGY = 0

outFile = "a.dml";

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

#These lists will hold the following information:
#    currentLines - The current file, loaded into an array of lines
#    labels - A list of labels
#    linesToResolve - A list of lines that need their labels to be resolved
currentLines = []
labels = []
linesToResolve = []

with open(fileName, "r") as File:
    for line in File:
        if(len(line.split(";")) > 1):
            currentLines.append(line.strip().upper().split(";")[0])

#This will hold the output
currentAddress = 0
output = [None] * 65535

#List Output
listOutput = [None] * 65535
listIndex = 0

def processDirective(directive: str):
    global currentAddress
    global output
    global listOutput
    global listIndex

def convertReg(reg: str):
    if(reg == "A"):
        return REGA
    elif(reg == "B"):
        return REGB
    elif(reg == "X"):
        return REGX
    elif(reg == "Y"):
        return REGY

for line in currentLines:
    oldIndex = currentAddress
    if(line[0] == "."):
        processDirective(line);
    elif ";" in line:
        if len(line.split(";")[0]) == 0:
            continue
        line = line.split(";")[0]
    print(line)

    if(len(line) == 0):
        continue

    if(":" in line):
        curLab = [currentAddress, line.split(":")[0]]
        labels.append(curLab)
        continue
    
    if("#" in line):
        #This is an immediate instruction
        sublines = line.split(" ")
        ins = sublines[0]
        args = sublines[1:]
        if(ins == "ADD"):
            #Add
            insCode = 0xA8
            insCode |= convertReg(args[0])
            ImmVal = hex(args[1])[2::]
            output[currentAddress] = insCode
            output[currentAddress + 1] = ImmVal
            currentAddress += 2
            listOutput[listIndex] = line;
            listIndex += 2
        elif(ins == "SUB"):
            #Subtract
            insCode = 0xAC
            insCode |= convertReg(args[0])
            ImmVal = hex(args[1])[2::]
            output[currentAddress] = insCode
            output[currentAddress + 1] = ImmVal
            currentAddress += 2
            listOutput[listIndex] = line;
            listIndex += 2
        elif("LD" in ins):
            #Load
            insCode = 0xC4
            insCode |= convertReg(args[0])
            ImmVal = hex(args[1])[2::]
            output[currentAddress] = insCode
            output[currentAddress + 1] = ImmVal
            currentAddress += 2
            listOutput[listIndex] = line;
            listIndex += 2
        elif(ins == "CMP"):
            #Compare
            insCode = 0xE0
            insCode |= convertReg(args[0]) << 2
            ImmVal = hex(args[1])[2::]
            output[currentAddress] = insCode
            output[currentAddress + 1] = ImmVal
            currentAddress += 2
            listOutput[listIndex] = line;
            listIndex += 2
    elif("$" in line):
        sublines = line.split(" ")
        #This is a instruction that deals with memory
        ins = sublines[0]
        args = sublines[1:]
        if(ins == "ADD"):
            #Add
            insCode = 0xA0
            argA = regCode(args[0]) << 4 | regCode(args[1]) << 2;
        pass

    
