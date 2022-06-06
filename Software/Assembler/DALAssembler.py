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




#These lists will hold the following information:
#    currentLines - The current file, loaded into an array of lines
#    labels - A list of labels
#    linesToResolve - A list of lines that need their labels to be resolved
currentLines = []
labels = []
linesToResolve = []

#Open the file, read all the data.
with open(fileName, "r") as File:
    for line in File:
        currentLines.append(line.strip().upper())

#This will hold our output for the file
currentAddress = 0;
output = [""] * 65536

#This will hold the "listing" output
listOutput = [""] * 65536
listIndex = 0

#This function will process any line that begins with "."
def processDirective(directive):
    #If the directive is .ORG, we will set the current address to the value
    directive = directive.upper().strip().split(" ")
    if(directive == ".ORG"):
        orgAddress = 0
        try:
            orgAddress = int(directive[1], 16)
        except:
            #This must be refering to a label!
            orgAddress = labels[directive[1]]
        #If the address supplied not is out of range
        if(orgAddress < 0 or orgAddress > 0xFFFF):
            #The org address must be greater than the current address.
            if(orgAddress > currentAddress):
                currentAddress = orgAddress
            else:
                #If the address is less than the current address, then alert the user!
                assert "ORG address must be greater than current address!"
        else:
            #If the address is invalid, alert the user!
            assert "Error: Directive .ORG must be between 0 and 0xFFFF"
    #If the user is trying to define a label
    elif(directive == ".LBL"):
        #Get the label name
        label = directive[1::]
        #Check if the label already exists
        if(label in labels):
            assert "Label already exists!"
        #Check if the label is valid
        for char in requiredChars:
            if char in label:
                addrBELE = findBELEcode(currentAddress)
                labels.append([label, addrBELE[0], addrBELE[1]])
                return
        assert "Invalid label name!" #If the label is invalid, alert the user!
        
#For each line in the current lines array
for line in currentLines:
    oldIndex = currentAddress
    #Print out the line
    print(line)
    #If the line is blank, skip it
    if(len(line) == 0):
        continue
    #If the line is a comment, skip it
    if(line[0] == ";"):
        continue

    #If the line is a directive, process it
    if(line[0] == "."):
        processDirective(line)
    #Split the line into smaller parts
    sublines = line.split(" ")
    listOutput[listIndex] = line
    
    if line ==               "NOP":   #If the line is a "NOP" instruction, then add 0x00 to the output
        output[currentAddress] = "00"
        currentAddress+= 1
    elif line ==             "BRK": #If the line is a "BRK" instruction, then add 0xFF to the output
        output[currentAddress] = "FF"
        currentAddress += 1
    elif line ==             "RST": #If the line is a "RST" instruction, then add 0xF7 to the output
        output[currentAddress] = "F7"
        currentAddress += 1
    elif line ==             "HLT": #If the line is a "HLT" instruction, then add 0xF9 to the output
        output[currentAddress] = "F9"
        currentAddress += 1
    elif sublines[0] ==      "ADD": #If we are adding, then determine if it is an immediate, or a register
        #If the line is an immediate
        if("#" in sublines[-1]):
            #This is an immediate add!
            output[currentAddress] = 0x101010 << 2 #Add 0b101010 to the output (Shifted by 2), and find the register we want to use. Then or it to the output.
            if sublines[1] == "A":
                output[currentAddress] = output[currentAddress] | REGA
            elif sublines[1] == "B":
                    output[currentAddress] = output[currentAddress] | REGB
            elif sublines[1] == "X":
                output[currentAddress] = output[currentAddress] | REGX
            elif sublines[1] == "Y":
                output[currentAddress] = output[currentAddress] | REGY
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            output[currentAddress] = hex(sublines[-1][1:], 16)[2::] #Add the immediate to the output
            currentAddress += 1
        else:
            #This is a register add!
            output[currentAddress] = 0xA0   #Add 0b10100000 to the output, then determine the register, and "or" it to the output.
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            if sublines[1] == "A":
                output[currentAddress] = REGA
            elif sublines[1] == "B":
                output[currentAddress] = REGB
            elif sublines[1] == "X":
                output[currentAddress] = REGX
            elif sublines[1] == "Y":
                output[currentAddress] = REGY
            output[currentAddress] = output[currentAddress] << 4 #Shift the register to the left by 4, and find the next register.
            if sublines[2] == "A":
                output[currentAddress] = output[currentAddress] | REGA
            elif sublines[2] == "B":
                output[currentAddress] = output[currentAddress] | REGB
            elif sublines[2] == "X":
                output[currentAddress] = output[currentAddress] | REGX
            elif sublines[2] == "Y":
                output[currentAddress] = output[currentAddress] | REGY
            output[currentAddress] = output[currentAddress] << 2    #Shift the register to the left by 2.
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
    elif sublines[0] ==      "SUB": #Same as above, but for SUB
        if("#" in sublines[-1]):
            #This is an immediate sub!
            output[currentAddress] = 0xAC
            if sublines[1] == "A":
                output[currentAddress] = output[currentAddress] | REGA
            elif sublines[1] == "B":
                output[currentAddress] = output[currentAddress] | REGB
            elif sublines[1] == "X":
                output[currentAddress] = output[currentAddress] | REGX
            elif sublines[1] == "Y":
                output[currentAddress] = output[currentAddress] | REGY
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            output[currentAddress] = int(sublines[-1][1:], 16)
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
        else:
            #This is a register sub!
            output[currentAddress] = 0xA5
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            if sublines[1] == "A":
                output[currentAddress] = REGA
            elif sublines[1] == "B":
                output[currentAddress] = REGB
            elif sublines[1] == "X":
                output[currentAddress] = REGX
            elif sublines[1] == "Y":
                output[currentAddress] = REGY
            output[currentAddress] = output[currentAddress] << 4
            if sublines[2] == "A":
                output[currentAddress] = output[currentAddress] | REGA
            elif sublines[2] == "B":
                output[currentAddress] = output[currentAddress] | REGB
            elif sublines[2] == "X":
                output[currentAddress] = output[currentAddress] | REGX
            elif sublines[2] == "Y":
                output[currentAddress] = output[currentAddress] | REGY
            output[currentAddress] = output[currentAddress] << 2
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
    elif sublines[0] ==      "INC": #Same as above, but for INC
        if(sublines[-1] == "A" or sublines[-1] == "B" or sublines[-1] == "X" or sublines[-1] == "Y"):
            #This is a register inc!
            output[currentAddress] = 0xA2
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            if sublines[-1] == "A":
                output[currentAddress] = REGA
            elif sublines[-1] == "B":
                output[currentAddress] = REGB
            elif sublines[-1] == "X":
                output[currentAddress] = REGX
            elif sublines[-1] == "Y":
                output[currentAddress] = REGY
            output[currentAddress] = output[currentAddress] << 6
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
        else:
            #This is an memory inc!
            output[currentAddress] = 0xB4
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            output[currentAddress] = int(sublines[1][1::]) & 0x0F #Get the lower nibble
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            try:
                output[currentAddress] = int(output[currentAddress][1::]) >> 4 #Get the upper nibble
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
            except:
                output[currentAddress] = 0
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
    elif sublines[0] ==      "DEC": #Same as above, but for DEC
        if(sublines[-1] == "A" or sublines[-1] == "B" or sublines[-1] == "X" or sublines[-1] == "Y"):
           #This is a register dec!
            output[currentAddress] = 0xB7
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            if sublines[-1] == "A":
                    output[currentAddress] =  REGA
            elif sublines[-1] ==  "B":
                    output[currentAddress] = REGB
            elif sublines[-1] == "X":
                    output[currentAddress] = REGX
            elif sublines[-1] == "Y":
                    output[currentAddress] = REGY
                    break;
            output[currentAddress] = output[currentAddress] << 6
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
        else:
            #This is an memory dec!
            output[currentAddress] = 0xB8
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            output[currentAddress] = int(sublines[1][1::]) & 0x0F #Get the lower nibble
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            try:
                output[currentAddress] = int(output[currentAddress][1::]) << 4 #Get the upper nibble
            except:
                output[currentAddress] = "00"
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
    elif sublines[0][0] ==   "T": #Transfer command. We add 0xC0 to the output, then find the registers, and add them as xx00xx00 in the next memory location.
        print("Transfer!")
        #This is a transfer!
        output[currentAddress] = 0xC0
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
        if sublines[0][1] == "A":
            output[currentAddress] =  REGA
        elif sublines[0][1] == "B":
            output[currentAddress] =  REGB
        elif sublines[0][1] == "X":
            output[currentAddress] =  REGX
        elif sublines[0][1] == "Y":
            output[currentAddress] =  REGY
        output[currentAddress] = output[currentAddress] << 4
        if sublines[0][2] == "A":
            output[currentAddress] =  output[currentAddress] | REGA
        elif sublines[0][2] == "B":
            output[currentAddress] =  output[currentAddress] | REGB
        elif sublines[0][2] == "X":
            output[currentAddress] =  output[currentAddress] |REGX
        elif sublines[0][2] == "Y":
            output[currentAddress] =  output[currentAddress] |REGY
        output[currentAddress] = output[currentAddress] << 2
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
    elif sublines[0] ==      "JMP": #Calculate the jump address, and add it to the output.
        #This is a jump!
        output[currentAddress] = 0x70
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
        try:
            #This is an address Jump!
            addr = int(sublines[1], 16)
            BELECODE = findBELEcode(addr)
            output[currentAddress] = BELECODE[0]
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            output[currentAddress] = BELECODE[1]
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
        except:
            #This is a label Jump!
            if(sublines[1] not in labels):
                print("Label needs resolution!")
                linesToResolve.append([currentAddress, sublines[1], listIndex])
                currentAddress += 2
            else:
                output[currentAddress] = labels[sublines[1]] & 0x0F
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
                currentAddress += 1
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
                output[currentAddress] = labels[sublines[1]] >> 4
                currentAddress += 1
    elif sublines[0][0] == "S" and sublines[0][1] == "T": #Store command. We add 0b110011 to the output, then find the register, and "or" with the opcode. Then find the mem location. and store that.
        #This is a Store Command!
        reg = sublines[0][2]
        addr = sublines[1]
        output[currentAddress] = 0b110011 << 2
        if reg == "A":
            output[currentAddress] = output[currentAddress] | REGA
        elif reg == "B":
            output[currentAddress] = output[currentAddress] | REGB
        elif reg == "X":
            output[currentAddress] = output[currentAddress] | REGX
        elif reg == "Y":
            output[currentAddress] = output[currentAddress] | REGY
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
                #Get memory address:
        addressEnd = findBELEcode(addr)
        output[currentAddress] = addressEnd[1]
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
        output[currentAddress] = addressEnd[0]
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
    elif sublines[0][0] == "L" and sublines[0][1] == "D":   #Load command. We add 0b110010 to the output, then find the register, and "or" with the opcode. Then find the mem location, or immediate, and store that.
        if(not "#" in sublines[1]):
            print("Ld NON-IMM")
            #This is a Load Command (Non-imm)!
            reg = sublines[0][2]
            addr = sublines[1]
            output[currentAddress] = 0b110010 << 2
            if reg == "A":
                output[currentAddress] = output[currentAddress] | REGA
            elif reg == "B":
                output[currentAddress] = output[currentAddress] | REGB
            elif reg == "X":
                output[currentAddress] = output[currentAddress] | REGX
            elif reg == "Y":
                output[currentAddress] = output[currentAddress] | REGY
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            #Get memory address:
            try:
                addressEnd = findBELEcode(addr)
                output[currentAddress] = addressEnd[1]
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
                currentAddress += 1
                output[currentAddress] = addressEnd[0]
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
                currentAddress += 1
            except:
                if(addr not in labels):
                    linesToResolve.append([currentAddress, addr])
                    currentAddress += 2
                else:
                    addressEnd = findBELEcode(labels[addr])
                    output[currentAddress] = addressEnd[1]
                    output[currentAddress] = hex(int(output[currentAddress]))[2:]
                    currentAddress += 1
                    output[currentAddress] = addressEnd[0]
                    output[currentAddress] = hex(int(output[currentAddress]))[2:]
                    currentAddress += 1
        else:
            print("Ld IMM")
            #This is a Load Command (Imm)!
            reg = sublines[0][2]
            output[currentAddress] = 0b110001 << 2
            if reg == "A":
                output[currentAddress] = output[currentAddress] | REGA
            elif reg == "B":
                output[currentAddress] = output[currentAddress] | REGB
            elif reg == "X":
                output[currentAddress] = output[currentAddress] | REGX
            elif reg == "Y":
                output[currentAddress] = output[currentAddress] | REGY
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            #Get number:
            if(sublines[1][0] == "#"):
                num = sublines[1][1:]
                output[currentAddress] = num
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
                currentAddress += 1
    elif sublines[0] ==      "PSH":  #Push command. We add 0b11000001 to the output, then find the register, and add it to the next output space.
        #PUSH
        output[currentAddress] = 0b11000001
        currentAddress+=1
        if sublines[1] == "A":
            output[currentAddress] = REGA
        elif sublines[1] == "B":
            output[currentAddress] = REGB
        elif sublines[1] == "X":
            output[currentAddress] = REGX
        elif sublines[1] == "Y":
            output[currentAddress] =  REGY
        output[currentAddress] = output[currentAddress] << 6
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
    elif sublines[0] ==      "POP":  #Pop Command. We add 0b11000010 to the output, then find the register, and add it to the next output space.
        output[currentAddress] = 0b11000010
        currentAddress += 1
        if sublines[1] == "A":
            output[currentAddress] = REGA
        elif sublines[1] == "B":
            output[currentAddress] = REGB
        elif sublines[1] == "X":
            output[currentAddress] = REGX
        elif sublines[1] == "Y":
            output[currentAddress] = REGY
        output[currentAddress] = output[currentAddress] << 6
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
    elif sublines[0] ==      "CMP":  #Compare. Add 0b1110, then find the 2 registers, and add them into the output.
        if("#" in sublines[-1]):
            #This is an immediate comparison
            output[currentAddress] = 0b1110 << 2;
            if sublines[1] == "A":
                output[currentAddress] = output[currentAddress] | REGA
            elif sublines[1] == "B":
                output[currentAddress] = output[currentAddress] | REGB
            elif sublines[1] == "X":
                output[currentAddress] = output[currentAddress] | REGX
            elif sublines[1] == "Y":
                output[currentAddress] = output[currentAddress] | REGY
            output[currentAddress] = output[currentAddress] << 2;
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
        else:
            output[currentAddress] = 0x1101 << 2
            #We want our lower register to be the first register
            regA = sublines[1]
            regB = sublines[2]
            if(regA < regB):
                tmp = regA
                regA = regB
                regB = tmp
            if regA == "A":
                output[currentAddress] = output[currentAddress] | REGA
            elif regA == "B":
                output[currentAddress] = output[currentAddress] | REGB
            elif regA == "X":
                output[currentAddress] = output[currentAddress] | REGX
            elif regA == "Y":
                output[currentAddress] = output[currentAddress] | REGY
            output[currentAddress] = output[currentAddress] << 2
            if regB == "A":
                output[currentAddress] = output[currentAddress] | REGA
            elif regB == "B":
                output[currentAddress] = output[currentAddress] | REGB
            elif regB == "X":
                output[currentAddress] = output[currentAddress] | REGX
            elif regB == "Y":
                output[currentAddress] = output[currentAddress] | REGY
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
    elif sublines[0] ==      "BNE":  #Branch if not equal. Add 0x30, then find the label or address, and add it to the output.
        #Branch on Not Equal
        output[currentAddress] = 0x30
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
        try:
            #This is an address Jump!
            addr = int(sublines[1], 16)
            BELECODE = findBELEcode(addr)
            output[currentAddress] = BELECODE[0]
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            output[currentAddress] = BELECODE[1]
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
        except:
            #This is a label Jump!
            if(sublines[1] not in labels):
                linesToResolve.append([currentAddress, sublines[1]])
                currentAddress += 2
            else:
                output[currentAddress] = labels[sublines[1]] & 0x0F
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
                currentAddress += 1
                output[currentAddress] = labels[sublines[1]] >> 4
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
                currentAddress += 1
    elif sublines[0] ==      "BEQ":  #Branch if equal. Add 0x31, then find the label or address, and add it to the output.
        #Branch on Equal
        output[currentAddress] = 0x31
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
        try:
            #This is an address Jump!
            addr = int(sublines[1], 16)
            BELECODE = findBELEcode(addr)
            output[currentAddress] = BELECODE[0]
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            output[currentAddress] = BELECODE[1]
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
        except:
            #This is a label Jump!
            if(sublines[1] not in labels):
                linesToResolve.append([currentAddress, sublines[1]])
                currentAddress += 2
            else:
                output[currentAddress] = labels[sublines[1]] & 0x0F
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
                currentAddress += 1
                output[currentAddress] = labels[sublines[1]] >> 4
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
                currentAddress += 1
    elif sublines[0] ==      "JSR":  #Jump to subroutine. Add 0x8B, then find the label or address, and add it to the output.
        #Jump to Subroutine
        output[currentAddress] = 0x8B
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
        try:
            #This is an address Jump!
            addr = int(sublines[1], 16)
            BELECODE = findBELEcode(addr)
            output[currentAddress] = BELECODE[0]
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            output[currentAddress] = BELECODE[1]
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
        except:
            #This is a label Jump!
            if(sublines[1] not in labels):
                linesToResolve.append([currentAddress, sublines[1]])
                currentAddress += 2
            else:
                output[currentAddress] = labels[sublines[1]] & 0x0F
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
                currentAddress += 1
                output[currentAddress] = labels[sublines[1]] >> 4
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
                currentAddress += 1  
    elif sublines[0] ==      "JSE":  #Jump to subroutine if equal. Add 0x8C, then find the label or address, and add it to the output.
        #Jump to Subroutine if Equal
        output[currentAddress] = 0x8D
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
        try:
            #This is an address Jump!
            addr = int(sublines[1], 16)
            BELECODE = findBELEcode(addr)
            output[currentAddress] = BELECODE[0]
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            output[currentAddress] = BELECODE[1]
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
        except:
            #This is a label Jump!
            if(sublines[1] not in labels):
                linesToResolve.append([currentAddress, sublines[1]])
                currentAddress += 2
            else:
                output[currentAddress] = labels[sublines[1]] & 0x0F
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
                currentAddress += 1
                output[currentAddress] = labels[sublines[1]] >> 4
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
                currentAddress += 1
    elif sublines[0] ==      "JSN":  #Jump to subroutine if not equal. Add 0x8E, then find the label or address, and add it to the output.
        #Jump to Subroutine if Not Equal
        output[currentAddress] = 0x8E
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
        try:
            #This is an address Jump!
            addr = int(sublines[1], 16)
            BELECODE = findBELEcode(addr)
            output[currentAddress] = BELECODE[0]
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
            output[currentAddress] = BELECODE[1]
            output[currentAddress] = hex(int(output[currentAddress]))[2:]
            currentAddress += 1
        except:
            #This is a label Jump!
            if(sublines[1] not in labels):
                linesToResolve.append([currentAddress, sublines[1]])
                currentAddress += 2
            else:
                output[currentAddress] = labels[sublines[1]] & 0x0F
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
                currentAddress += 1
                output[currentAddress] = labels[sublines[1]] >> 4
                output[currentAddress] = hex(int(output[currentAddress]))[2:]
                currentAddress += 1
    elif sublines[0] ==      "RET":  #Return from subroutine. Add 0x8C.
        #Return from Subroutine
        output[currentAddress] = 0x8C
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
    elif sublines[0] ==      "MJB":  #Move Jump -> B. Move PC to B, 
        #Move PC to B
        output[currentAddress] = 0x74
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
    elif sublines[0] ==      "MBJ":  #Move B -> Jump. Move B to PC,
        #Move B to PC
        output[currentAddress] = 0x73
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
    elif sublines[0] ==      "LSR":  #Logical Shift Right. Add 0b01010100, then find the register, and add it to the output.
        output[currentAddress] = 0b010101 << 2
        if sublines[1] == "A":
            output[currentAddress] = output[currentAddress] | REGA
        elif sublines[1] == "B":
            output[currentAddress] = output[currentAddress] | REGB
        elif sublines[1] == "X":
            output[currentAddress] = output[currentAddress] | REGX
        elif sublines[1] == "Y":
            output[currentAddress] = output[currentAddress] | REGY
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
        currentAddress += 1
    elif sublines[0] ==      "LSL":  #Logical Shift Left. Add 0b010100, then find the register, and add it to the output.
        output[currentAddress] = 0b010100 << 2
        if sublines[1] == "A":
            output[currentAddress] = output[currentAddress] | REGA
        elif sublines[1] == "B":
            output[currentAddress] = output[currentAddress] | REGB
        elif sublines[1] == "X":
            output[currentAddress] = output[currentAddress] | REGX
        elif sublines[1] == "Y":
            output[currentAddress] = output[currentAddress] | REGY
        output[currentAddress] = hex(int(output[currentAddress]))[2:]
    listIndex += (currentAddress - oldIndex)

#If we have any unresolved labels, we need to resolve them now.
print(linesToResolve)
for line in range(len(linesToResolve)):
    print(linesToResolve[line])
    for label in labels:
        if(label[0] == linesToResolve[line][1]):
            output[linesToResolve[line][0]] = label[1]
            output[linesToResolve[line][0] + 1] = label[2]
            break

#Write output to files
for extension in fileExtensions:
    #If we are writing to a "bin" file:
    if(extension == ".bin"):
        #Open the file
        with open(outFile + extension, "wb") as file:
            #for each line in the output
            for line in output:
                #Try to write the line to the file
                if(line == ""):
                    continue
                file.write(bytes(chr(int(line, 16)), encoding="utf-8"))
    else:
        with open(outFile + extension, "w") as file:
            #If we are writing to a "lst" file:
            if(extension == ".lst"):
                #Write the heading for the file.
                file.write("ML\t\tASM\n")
                file.write("______________________\n")

                #for each line in the output
                for index in range(len(listOutput)):
                    #If the line is blank, continue.
                    if(output[index] == ''):
                        file.write("00\n")
                        continue
                    #Otherwise, write to the file the hex value of the line, and the disassembled line.
                    outputHex = str(output[index]).upper()
                    while len(outputHex) < 2:
                        outputHex = "0" + outputHex
                    file.write(outputHex + "\t\t" + str(listOutput[index]) + "\n")
                    if(output[index] == ""):
                        file.write("\n")
            if(extension == ".txt"):
                for line in output:
                    if(line == ""):
                        file.write("00\n")
                    else:
                        while len(line) < 2:
                            line = "0" + line
                        file.write(str(line) + "\n")
    