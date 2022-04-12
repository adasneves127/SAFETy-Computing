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

import sys, binascii

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

with open(fileName, "r") as File:
    for line in File:
        currentLines.append(line.strip())

