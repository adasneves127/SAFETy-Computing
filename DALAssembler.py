#Machine Code:
#ADD:
#   (10100000 xx00xx00)              A0 (R1)(R2) -- Add 2 registers
#   (101010xx ########)              A (0b10) (R1) (I1 (8b)) -- Add Immediate
#    
#
#SUB:
#    (10100101 xx00xx00)             A5 (R1)(R2) -- Subtract R2 from R1
#    (101001xx ########)             A (0b01) (R1)  (I1 (8b)) -- Subtract Immediate
#    
#
#INC:
#    (10100010 xx000000)             A2 (R1) 00  -- Increment R1 
#    (10110100 $$$$$$$$ $$$$$$$$)    B4 (MEM) -- Increment Memory Address
#    
#
#DEC:
#    (10110111 xx000000)             B7 (R1) 00 -- Decrement R1
#    (10111111 $$$$$$$$ $$$$$$$$)    B8 (MEM) -- Decrement Memory Address
#
#
#TRANSFER:
#    (11000000 xx00xx00)             C0 (R1) 00 (R2) 00
#
#PSH:
#    (11000001 xx000000)             C1 (R1)
#
#POP:
#    (11000010 xx000000)             C2 (R1)
#
#LOAD:
#                                    (4, 5, 5, 6)
#    (110001xx ########)             C (0b01) (R1)   (I1 (8b))
#
#                                    (8, 9, A, B)
#    (110010xx $$$$$$$$ $$$$$$$$)    C (0b10) (R1)   (MEM) 0000
#
#ST:
#                                    (C, D, E, F)
#    (110011xx $$$$$$$$ $$$$$$$$)    C (0b11) (R1)   (MEM)
#
#Comparing and Branching:
#CMP:
#    (1101xxxx)                      D (R1) (R2)  -- Compare 2 registers
#
#CPI:
#    (1110 xx00 ########)            E (0b01) (R1) (I1) -- Compare 1 register and 1 immediate
#
#BNE
#    (00110000 $$$$$$$$ $$$$$$$$)    30 (Mem) -- Branch if last result did not produce a zero
#
#BEQ
#    (00110001 $$$$$$$$ $$$$$$$$)    31 (Mem) -- Branch if last result did produce a zero
#
#JSR
#    (10001011 $$$$$$$$ $$$$$$$$)    8B (Mem)
#
#JSE
#    (10001101 $$$$$$$$ $$$$$$$$)    8D (Mem) -- JSR on Equals
#
#JSN
#    (10001110 $$$$$$$$ $$$$$$$$)    8E (Mem) -- JSR on Not Equals
#
#RET
#    (10001100)                      8C
#
#JMP 
#    (01110000 $$$$$$$$ $$$$$$$$)    70 (Mem)
#
#
#MJB
#    Move Program Counter to B Register
#
#MBJ
#    Jump to address in B Register
#
#NOP -- No Operation
#    00
#
#BRK -- Break
#    FF
#
#HLT -- Halt the CPU
#    F9
#
#RST -- Reset
#    F7

from calendar import c
import sys, binascii

REGA = 0
REGB = 1
REGX = 2
REGY = 3

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


currentLines = []
labels = {}
linesToResolve = []

with open(fileName, "r") as File:
    for line in File:
        currentLines.append(line.strip().upper())

currentAddress = 0;
output = [""] * 65325

def processDirective(directive):
    directive = directive.upper().strip().split(" ")
    if(directive == ".ORG"):
        orgAddress = 0
        try:
            orgAddress = int(directive[1], 16)
        except:
            #This must be refering to a label!
            orgAddress = labels[directive[1]]
        if(orgAddress < 0 or orgAddress > 0xFFFF):
            if(orgAddress > currentAddress):
                currentAddress = orgAddress
            else:
                assert "ORG address must be greater than current address!"
        else:
            assert "Error: Directive .ORG must be between 0 and 0xFFFF"
    elif(directive == ".LBL"):
        label = directive[1]
        if(label in labels):
            assert "Label already exists!"
        labels[label] = currentAddress



for line in currentLines:
    print(line)
    sublines = line.split(" ")
    if line == "NOP":
        output[currentAddress] = 00
        currentAddress+= 1
    elif line == "BRK":
        output[currentAddress] = 0xFF
        currentAddress += 1
    elif line == "RST":
        output[currentAddress] = 0xF7
        currentAddress += 1
    elif line == "HLT":
        output[currentAddress] = 0xF9
        currentAddress += 1
    elif line == "ADD":
        if("#" in sublines[-1]):
            #This is an immediate add!
            output[currentAddress] = 0xA0
            match sublines[1]:
                case "A":
                    output[currentAddress] = output[currentAddress] | REGA
                    break;
                case "B":
                    output[currentAddress] = output[currentAddress] | REGB
                    break;
                case "X":
                    output[currentAddress] = output[currentAddress] | REGX
                    break;
                case "Y":
                    output[currentAddress] = output[currentAddress] | REGY
                    break;
            currentAddress += 1
            output[currentAddress] = int(sublines[-1][1:], 16)
            currentAddress += 1
        else:
            #This is a register add!
            output[currentAddress] = 0xA0
            currentAddress += 1
            match sublines[1]:
                case "A":
                    output[currentAddress] = output[currentAddress] | REGA
                    break;
                case "B":
                    output[currentAddress] = output[currentAddress] | REGB
                    break;
                case "X":
                    output[currentAddress] = output[currentAddress] | REGX
                    break;
                case "Y":
                    output[currentAddress] = output[currentAddress] | REGY
                    break;
            output[currentAddress] = output[currentAddress] << 4
            match sublines[2]:
                case "A":
                    output[currentAddress] = output[currentAddress] | REGA
                    break;
                case "B":
                    output[currentAddress] = output[currentAddress] | REGB
                    break;
                case "X":
                    output[currentAddress] = output[currentAddress] | REGX
                    break;
                case "Y":
                    output[currentAddress] = output[currentAddress] | REGY
                    break;
            output[currentAddress] = output[currentAddress] << 2
            currentAddress += 1
    elif line == "SUB":
        if("#" in sublines[-1]):
            #This is an immediate sub!
            output[currentAddress] = 0xAC
            match sublines[1]:
                case "A":
                    output[currentAddress] = output[currentAddress] | REGA
                    break;
                case "B":
                    output[currentAddress] = output[currentAddress] | REGB
                    break;
                case "X":
                    output[currentAddress] = output[currentAddress] | REGX
                    break;
                case "Y":
                    output[currentAddress] = output[currentAddress] | REGY
                    break;
            currentAddress += 1
            output[currentAddress] = int(sublines[-1][1:], 16)
            currentAddress += 1
        else:
            #This is a register sub!
            output[currentAddress] = 0xA5
            currentAddress += 1
            match sublines[1]:
                case "A":
                    output[currentAddress] = output[currentAddress] | REGA
                    break;
                case "B":
                    output[currentAddress] = output[currentAddress] | REGB
                    break;
                case "X":
                    output[currentAddress] = output[currentAddress] | REGX
                    break;
                case "Y":
                    output[currentAddress] = output[currentAddress] | REGY
                    break;
            output[currentAddress] = output[currentAddress] << 4
            match sublines[2]:
                case "A":
                    output[currentAddress] = output[currentAddress] | REGA
                    break;
                case "B":
                    output[currentAddress] = output[currentAddress] | REGB
                    break;
                case "X":
                    output[currentAddress] = output[currentAddress] | REGX
                    break;
                case "Y":
                    output[currentAddress] = output[currentAddress] | REGY
                    break;
            output[currentAddress] = output[currentAddress] << 2
            currentAddress += 1
    elif line == "INC":
        if(sublines[-1] == "A" or sublines[-1] == "B" or sublines[-1] == "X" or sublines[-1] == "Y"):
            #This is a register inc!
            output[currentAddress] = 0xA2
            currentAddress += 1
            match sublines[-1]:
                case "A":
                    output[currentAddress] = output[currentAddress] | REGA
                    break;
                case "B":
                    output[currentAddress] = output[currentAddress] | REGB
                    break;
                case "X":
                    output[currentAddress] = output[currentAddress] | REGX
                    break;
                case "Y":
                    output[currentAddress] = output[currentAddress] | REGY
                    break;
            output[currentAddress] = output[currentAddress] << 6
            currentAddress += 1
        else:
            #This is an memory inc!
            output[currentAddress] = 0xB4
            currentAddress += 1
            output[currentAddress] = sublines[1] & 0x0F #Get the lower nibble
            currentAddress += 1
            output[currentAddress] = output[currentAddress] << 4 #Get the upper nibble
            currentAddress += 1
    elif line == "DEC":
        if(sublines[-1] == "A" or sublines[-1] == "B" or sublines[-1] == "X" or sublines[-1] == "Y"):
           #This is a register dec!
            output[currentAddress] = 0xB7
            currentAddress += 1
            match sublines[-1]:
                case "A":
                    output[currentAddress] = output[currentAddress] | REGA
                    break;
                case "B":
                    output[currentAddress] = output[currentAddress] | REGB
                    break;
                case "X":
                    output[currentAddress] = output[currentAddress] | REGX
                    break;
                case "Y":
                    output[currentAddress] = output[currentAddress] | REGY
                    break;
            output[currentAddress] = output[currentAddress] << 6
            currentAddress += 1
        else:
            #This is an memory dec!
            output[currentAddress] = 0xB8
            currentAddress += 1
            output[currentAddress] = sublines[1] & 0x0F #Get the lower nibble
            currentAddress += 1
            output[currentAddress] = output[currentAddress] << 4 #Get the upper nibble
            currentAddress += 1
    elif line[0] == "T":
        #This is a transfer!
        output[currentAddress] = 0xC0
        currentAddress += 1
        match sublines[1]:
            case "A":
                output[currentAddress] = output[currentAddress] | REGA
                break;
            case "B":
                output[currentAddress] = output[currentAddress] | REGB
                break;
            case "X":
                output[currentAddress] = output[currentAddress] | REGX
                break;
            case "Y":
                output[currentAddress] = output[currentAddress] | REGY
                break;
        output[currentAddress] = output[currentAddress] << 4
        match sublines[2]:
            case "A":
                output[currentAddress] = output[currentAddress] | REGA
                break;
            case "B":
                output[currentAddress] = output[currentAddress] | REGB
                break;
            case "X":
                output[currentAddress] = output[currentAddress] | REGX
                break;
            case "Y":
                output[currentAddress] = output[currentAddress] | REGY
                break;
        output[currentAddress] = output[currentAddress] << 2
        currentAddress += 1
    elif line == "JMP":
        #This is a jump!
        try:
            #This is an address Jump!
            int(sublines[1])
        except:
            #This is a label Jump!
            if(sublines[1] not in labels):
                linesToResolve.append(currentAddress)
            else:
                output[currentAddress] = labels[sublines[1]] & 0x0F
                currentAddress += 1
                output[currentAddress] = labels[sublines[1]] >> 4
                currentAddress += 1
