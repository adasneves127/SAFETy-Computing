# Read Me

This repository contains code to interpret and execute a custom assembly code. The specific assembly code is provided in the 'assembly.txt' file. 

To convert assembly code into machine code, use DALAssembler.py.

Memory Addresses are stored in the 'memory.txt' file.
All memory addresses are stored in hexadecimal. All addresses are 16 bits long.
Each memory address stores 8 bits of data.

### Assembly

Assembly files have the file extension of .DAL

### Machine Code

Machine code files end with .dal.txt, .dal.lst, and .dal.bin. Addresses in MC are Little Endian.

## Assembler
To use the assembler, run the script as python3, and supply an input file.

ex: python3 DALAssembler.py \<-o outputFile> inputFile

## Simulator

To run the simulator, first off, compile it with GCC or Clang.

ex: gcc -o simulator simulator.c

After that, run it with ./simulator \<input file\>

# Change Log

All noteable changes for this project will be documented within this file.

## [V 1.0]

### Added

- Layed out formatting for Assembly

- Layed out conversion from Assembly to Machine

- Created Instruction Set V1

- Created gitignore file

## [V 1.3]

### Added

#### Scripting

- Created DALAssembler.py
    - Usage:
    >python3 DALAssembler <-o outputFile> inputFile

    - DALAssembler.py generates 3 files.

      - File 1: DAL.bin
  
        - This is a direct binary file, used for programming ROMS

      - File 2: DAL.lst
  
        - This file shows the Machine Code against the Assembly Code. 

      -  File 3: DAL.txt
         -  This file will show the machine code in direct text.
  
#### Language

- Added New Branching Commands

#### Files:

- Added Changelog.md


## [V1.4]

### Added

- V1 of the Simulator
- Added more instructions to the compiler
  
## [V1.5]

### Added

- Added to gitignore all test.*

### Changed

- Revamped memory structuring

### Removed

- Removed memory page instructions

## [V1.6.1]

### Added

- Added more instructions to the compiler

### Removed
- Removed Java simulator. This is to be changed into C.

### Changed
- Changed instruction codes to prevent potential conflicts.

## Simulator Status
* Simulator Prototype built in Java
  * System Monitor graphical Display Designed
* Simulator Language changed to Changelog

##  [V1.6.2]

### Added
- Added more instructions to the assembler
- Added Changed changelog to ReadMe.md