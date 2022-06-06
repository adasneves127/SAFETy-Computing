import assemblyDef   #This is the file that contains the assembly instructions
import sys           #This is the file that contains the command line arguments
import re

fileName = ""
inputLines = []

#Output Lines:
# [Address, Operation, Arguments, Machine Code]
outputLines = [0] * 0xFFFF
outputIndex = 0
linesToResolve = []
labelsToResolve = []

#AssemblyDef includes the following:
#   A dictionary of all assembly conversions to the machine code.
#   A dictionary of all reserverd labels to their location in memory
#   A dictionary of all reserved variables to their location in memory

def writeFiles():
    pass

def assemble():
    global inputLines, outputLines, outputIndex, linesToResolve, labelsToResolve
    for ind, data in enumerate(inputLines):
        if("." in data):
            pass #This will be a directive. We will need to fix it later.
            continue
        if(":" in data):
            labelsToResolve.append([outputIndex, data])
            continue
        splitLine = data.split(" ")
        instruction = splitLine[0]
        isJump = re.match("(jmp|beq|bne|jsn|jse|jsr)", data)
        if type(isJump) != None: #If it is a jump instruction, or it's derivates
            linesToResolve.append([outputIndex, instruction, splitLine[1::]])
            outputIndex += 3 #We will need to add 3 to the index, as all jump instructions are 3 bytes long. We will come back to it later.
            continue
        try:
            outputLines[outputIndex] = assemblyDef.assemblyDict[instruction][0]
            outputIndex += assemblyDef.assemblyDict[instruction][1]
        except KeyError:
            print("Error: Invalid instruction: " + instruction)
            sys.exit(1)
        
    writeFiles()

def readIn():
    global inputLines
    #Open the file
    with open(fileName) as fileIn:
        for line in fileIn:
            inputLines.append(line.lower())
    assemble()

def getStartData():
    global fileName
    debug = False
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
        DAL Assembly Tool V3
                Usage: DALAssembler.py [-o <output file>] <input file>
                -o <output file> - Specify the output file.
                <input file> - Specify the input file.
                -h - Print this help message.
                
        Designed By: Alex Dasneves
        """)
                sys.exit(0)
        #If the user did not supply a valid output file
        if(type(re.match(".*\.aspect", sys.argv[len(sys.argv)-1])) == None):
            print("Invalid file extension or no file specified!")
            sys.exit(1)
        #Set the file name
        fileName = sys.argv[len(sys.argv) - 1]
        #fileName = "testProgram.dal"
    else:
        #If we are debugging, just set the output to be test.dal
        fileName = "test.aspect"
    readIn()

getStartData()