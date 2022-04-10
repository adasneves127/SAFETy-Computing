# ---------------------------------------------------------------------------- #
#                             Assembly Conversions                             #
# ---------------------------------------------------------------------------- #
#ADD   
#   (10100000 xx00xx00)              A0 (R1)(R2) -- Add 2 registers
#   (101010xx ########)              A1 (0b10) (R1) (I1 (8b)) -- Add Immediate
#
#SUB
#   (10100101 xx00xx00)             A5 (R1)(R2) -- Subtract R2 from R1
#   (101001xx $$$$$$$$ ########)    A6 (0b01) (R1)  (I1 (8b)) -- Subtract Immediate
#
#INC
#   (10100010 xx000000)             A2 (R1) 00  -- Increment R1 
#   (10100100 $$$$$$$$ $$$$$$$$)    A4 (MEM) -- Increment Memory Address
#
#DEC
#   (10100111 xx000000)             A7 (R1) 00 -- Decrement R1
#   (10101111 $$$$$$$$ $$$$$$$$)    A8 (MEM) -- Decrement Memory Address
#
#Transfer
#   (11000000 xx00xx00)             C0 (R1) 00 (R2) 00
#
#Push
#   (11000001 xx000000)             C1 (R1)
#
#Pop
#   (11000010 xx000000)             C2 (R1)
#
#LOAD                                 (4, 5, 5, 6)
#   (110001xx ########)             C (0b01) (R1)   (I1 (8b))
#                                     (8, 9, A, B)
#   (110010xx $$$$$$$$)             C (0b10) (R1)   (MEM) 0000
#
#Store:
#                                     (C, D, E, F)
#   (110011xx $$$$$$$$ $$$$$$$$)    C (0b11) (R1)   (MEM)
#
#CMP
#   (1101xxxx)                      D (R1) (R2)  -- Compare 2 registers
#
#CPI
#   (1110 xx00 ########)            E (0b01) (R1) (I1) -- Compare 1 register and 1 immediate
#
#BNE
#   (00110000 $$$$$$$$ $$$$$$$$)    30 (Mem) -- Branch if last result did not produce a zero
#
#BEQ
#    (00110001 $$$$$$$$ $$$$$$$$)   31 (Mem) -- Branch if last result did produce a zero
#
#JSR
#   (10001011 $$$$$$$$ $$$$$$$$)   8B (Mem) -- Jump to Subroutine
#
#RTS
#   (10001100 $$$$$$$$ $$$$$$$$)   8C (Mem) -- Return from Subroutine
#
#JSB (Jump to Subroutine (Branch))
#   (10001101 $$$$$$$$ $$$$$$$$)   8D (Mem) -- Jump to Subroutine
#
#Increment Mem Page
#   (11110000)                      F0
#
#Decrement Mem Page
#   (11110001)                      F1
#   
#---------------------------------------------------------------------------- #

import sys
import binascii

inputLines = [""] * 65536
directiveAddresses = []

labelAddresses = {}

CurrentAddress = 0

outputListing = {}
output = [""] * 65536

def processDirective(directive):
    global output
    global labelAddresses
    global CurrentAddress
    global directiveAddresses
    directive = directive.strip().split()
    
    if(directive[0].upper() == ".ORG"):
        if (int(directive[1]) < CurrentAddress):
            print("Error: .ORG address must be greater than current address")
            print("Current Address: " + str(CurrentAddress))
            print(".ORG Address: " + str(directive[1]))
            sys.exit(1)
        CurrentAddress = int(directive[1])
    pass

outFile = "a.dml"

argumentsFound = 0

fileExtensions = [
    ".bin",
    ".txt",
    ".lst"
]
if(len(sys.argv) == 1):
    print("No file specified")
    sys.exit(1)

for argIndex in range(1, len(sys.argv)):
    if(sys.argv[argIndex] == "-o"):
        outFile = sys.argv[argIndex + 1]
        argumentsFound += 2
    elif(sys.argv[argIndex] == "-h"):
        print("""
DAL Assembly Tool
        Usage: DALAssembler.py [-o <output file>] <input file>
        -o <output file> - Specify the output file.
        <input file> - Specify the input file.
        -h - Print this help message.
        
Designed By: Alex Dasneves
""")
        sys.exit(0)
   
if(not ".dal" in sys.argv[len(sys.argv) - 1]):
    print("Invalid file extension or no file specified!")
    sys.exit(1)


fileName = sys.argv[len(sys.argv) - 1]
#fileName = "testProgram.dal"


with open(fileName) as fileReader:
    for line in fileReader:
        inputLines[CurrentAddress] = line
        #Convert ASM to key components
        if(line.startswith(";")):
            continue
        if line.startswith("."):
            processDirective(line)
        currentInstruction = ""
        isImmediate = False;
        RegisterA = ""
        RegisterB = ""
        MemAddress = 0
        currentLine = line.split(" ")
        
        for index in range(0, len(currentLine)):
            currentLine[index] = currentLine[index].strip()
        Instruction = currentLine[0].upper()
        #Load
        if "LD" in Instruction:
            currentInstruction = "LOAD"
            RegisterA = Instruction[-1]
            
            if("#" in currentLine[1]):
                isImmediate = True
                currentLine[1] = currentLine[1].replace("#", "")
        #Store
        elif "ST" in Instruction:
            currentInstruction = "STORE"
            RegisterA = Instruction[-1]
        #Increment Mem Page
        elif Instruction == "IMP":
            currentInstruction = "IMP"
        #Decrement Mem Page
        elif Instruction == "DMP":
            currentInstruction = "DMP"
        #Add
        elif Instruction == "ADD":
            if("#" in currentLine[2]):
                currentInstruction = "ADD"
                isImmediate = True
            else:
                currentInstruction = "ADD"
        elif Instruction == "SUB":
            if("#" in currentLine[2]):
                currentInstruction = "SUB"
                isImmediate = True
            else:
                currentInstruction = "SUB"
        elif Instruction == "INC":
            currentInstruction = "INC"
            if(len(currentLine[1]) == 2):
                RegisterA = currentLine[1]
            else:
                MemAddress = hex(int(currentLine[1]) << 8).split("0x")[1] + str(currentLine[2].split("0x")[1])
        elif Instruction == "DEC":
            currentInstruction = "DEC"
            if(len(currentLine) == 2):
                RegisterA = currentLine[1]
            else:
                MemAddress = hex(int(currentLine[1]) << 8).split("0x")[1] + hex(int(currentLine[2])).split("0x")[1]
                
        elif Instruction == "PSH":
            currentInstruction = "PSH"
            RegisterA = currentLine[1]
        elif Instruction == "POP":
            currentInstruction = "POP"
            RegisterA = currentLine[1]
        elif Instruction == "CMP":
            currentInstruction = "CMP"
            if(len(currentLine) == 1):
                RegisterA = currentLine[1]
                RegisterB = currentLine[2]
            else:
                isImmediate = True;
        

        #Convert Key Components to ML
        match currentInstruction:
            case "LOAD":
                #(110001xx ########)      
                #(110010xx $$$$$$$$)
                if(isImmediate):
                    match RegisterA:
                        case "A":
                            output[CurrentAddress] = hex(0b11000100).split("0x")[1]
                            
                        case "B":
                            output[CurrentAddress] = hex(0b11000101).split("0x")[1]
                        case "X":
                            output[CurrentAddress] = hex(0b11000110).split("0x")[1]
                        case "Y":
                            output[CurrentAddress] = hex(0b11000111).split("0x")[1]
                    CurrentAddress += 1
                    output[CurrentAddress] = currentLine[1]
                    CurrentAddress += 1
                else:
                    match RegisterA:
                        case "A":
                            output[CurrentAddress] = hex(0b11001000).split("0x")[1]
                        case "B":
                            output[CurrentAddress] = hex(0b11001001).split("0x")[1]
                        case "X":
                            output[CurrentAddress] = hex(0b11001010).split("0x")[1]
                        case "Y":
                            output[CurrentAddress] = hex(0b11001011).split("0x")[1]
                    CurrentAddress += 1
                    output[CurrentAddress] = currentLine[1]
                    CurrentAddress += 1
            case "STORE":
                 #(110011xx $$$$$$$$) #0b11001100
                match RegisterA:
                    case "A":
                        output[CurrentAddress] = hex(0b11001100).split("0x")[1]
                    case "B":
                        output[CurrentAddress] = hex(0b11001101).split("0x")[1]
                    case "X":
                        output[CurrentAddress] = hex(0b11001110).split("0x")[1]
                    case "Y":
                        output[CurrentAddress] = hex(0b11001111).split("0x")[1]
                CurrentAddress += 1
                output[CurrentAddress] = currentLine[1]
                CurrentAddress += 1
            case "IMP":
                output[CurrentAddress] = hex(0b11110000).split("0x")[1]
                CurrentAddress += 1
            case "DMP":
                output[CurrentAddress] = hex(0b11110001).split("0x")[1]
                CurrentAddress += 1
            case "ADD":
                if isImmediate: #0b10101000
                    match RegisterA:
                        case "A":
                            output[CurrentAddress] = hex(0b10101000).split("0x")[1]
                        case "B":
                            output[CurrentAddress] = hex(0b10101001).split("0x")[1]
                        case "X":
                            output[CurrentAddress] = hex(0b10101010).split("0x")[1]
                        case "Y":
                            output[CurrentAddress] = hex(0b10101011).split("0x")[1]
                    CurrentAddress += 1
                    output[CurrentAddress] = currentLine[1]
                    CurrentAddress += 1
                else:
                    currLineInstruction = ""
                    output[CurrentAddress] = hex(0b10100011).split("0x")[1]
                    CurrentAddress += 1
                    match RegisterA:
                        case "A":
                            currLineInstruction += hex(0b0000).split("0x")[1]
                        case "B":
                            currLineInstruction += hex(0b0100).split("0x")[1]
                        case "X":
                            currLineInstruction += hex(0b1000).split("0x")[1]
                        case "Y":
                            currLineInstruction += hex(0b1100).split("0x")[1]
                    match RegisterB:
                        case "A":
                            currLineInstruction += hex(0b0000).split("0x")[1]
                        case "B":
                            currLineInstruction += hex(0b0100).split("0x")[1]
                        case "X":
                            currLineInstruction += hex(0b1000).split("0x")[1]
                        case "Y":
                            currLineInstruction += hex(0b1100).split("0x")[1]
                    output[CurrentAddress] = currLineInstruction
                    CurrentAddress += 1
            case "INC":
                if(MemAddress == 0):
                    output[CurrentAddress] = hex(0b10100010).split("0x")[1]
                    CurrentAddress += 1
                    match(RegisterA):
                        case "A":
                            output[CurrentAddress] = hex(0b00000000).split("0x")[1]
                        case "B":
                            output[CurrentAddress] = hex(0b01000000).split("0x")[1]
                        case "X":
                            output[CurrentAddress] = hex(0b10000000).split("0x")[1]
                        case "Y":  
                            output[CurrentAddress] = hex(0b11000000).split("0x")[1]
                    CurrentAddress += 1
                else:
                    output[CurrentAddress] = hex(0b10100100).split("0x")[1]
                    CurrentAddress += 1
                    output[CurrentAddress] = MemAddress
                    CurrentAddress += 1
            case "DEC":
                if(MemAddress == 0):
                    output[CurrentAddress] = hex(0b10100011).split("0x")[1]
                    CurrentAddress += 1
                    match(RegisterA):
                        case "A":
                            output[CurrentAddress] = hex(0b00000000).split("0x")[1]
                        case "B":
                            output[CurrentAddress] = hex(0b01000000).split("0x")[1]
                        case "X":
                            output[CurrentAddress] = hex(0b10000000).split("0x")[1]
                        case "Y":
                            output[CurrentAddress] = hex(0b11000000).split("0x")[1]
                    CurrentAddress += 1
                else:
                    output[CurrentAddress] = hex(0b10101111).split("0x")[1]
                    CurrentAddress += 1
                    output[CurrentAddress] = hex(MemAddress).split("0x")[1]
                    CurrentAddress += 1
            case "PSH":
                output[CurrentAddress] = hex(0b11000001).split("0x")[1]
                CurrentAddress += 1
                match RegisterA:
                    case "A":
                        output[CurrentAddress] = hex(0b00000000).split("0x")[1]
                    case "B":
                        output[CurrentAddress] = hex(0b01000000).split("0x")[1]
                    case "X":
                        output[CurrentAddress] = hex(0b10000000).split("0x")[1]
                    case "Y":
                        output[CurrentAddress] = hex(0b11000000).split("0x")[1]
                CurrentAddress += 1
            case "POP":
                output[CurrentAddress] = hex(0b11000010).split("0x")[1]
                CurrentAddress += 1
                match RegisterA:
                    case "A":
                        output[CurrentAddress] = hex(0b00000000).split("0x")[1]
                    case "B":
                        output[CurrentAddress] = hex(0b01000000).split("0x")[1]
                    case "X":
                        output[CurrentAddress] = hex(0b10000000).split("0x")[1]
                    case "Y":
                        output[CurrentAddress] = hex(0b11000000).split("0x")[1]
                CurrentAddress += 1
            case "CMP":
                if isImmediate: 
                    regA = 0
                    match RegisterA:
                        case "A":
                            regA = 0
                        case "B":
                            regA = 1
                        case "X":
                            regA = 2
                        case "Y":
                            regA = 3
                    output[CurrentAddress] = str(int(hex(0b1110).split("0x")[1]) << 4) + str(hex(regA).split("0x")[1]) + "00"
                    CurrentAddress += 1
                    output[CurrentAddress] = currentLine[1]
                    CurrentAddress += 1
                    pass
                else:
                    regA = 0
                    regB = 0
                    match RegisterA:
                        case "A":
                            regA = 0
                        case "B":
                            regA = 1
                        case "X":
                            regA = 2
                        case "Y":
                            regA = 3
                    match RegisterB:
                        case "A":
                            regB = 0
                        case "B":
                            regB = 1
                        case "X":
                            regB = 2
                        case "Y":
                            regB = 3

                    output[CurrentAddress] = str(int(hex(0b1101).split("0x")[1]) << 4) + str(int(hex(regA).split("0x")[1]) << 2) + str(int(hex(regB).split("0x")[1]))
                    CurrentAddress += 1

for lineIndex in range(len(output)):
    output[lineIndex] = output[lineIndex].strip().upper()
    hexPrefix = hex(lineIndex).split("0x")[1]
    if(len(hexPrefix) < 4):
        hexPrefix = "0" * (4 - len(hexPrefix)) + hexPrefix
    
    print(hexPrefix+ ": " + output[lineIndex])
            
for extension in fileExtensions:
    if(extension == ".bin"):
        with open(fileName + extension, "wb") as file:
            for line in output:
                file.write(binascii.unhexlify(line))
        continue
    with open(fileName + extension, "w") as file:
        if(extension == ".lst"):
            file.write("ML\t\tASM\n")
            file.write("______________________\n")
            for index in range(len(output)):
                file.write(output[index] + "\t\t" + inputLines[index])
                if(output[index] == ""):
                    file.write("\n")
        if(extension == ".txt"):
            for line in output:
                file.write(line + "\n")
        
           