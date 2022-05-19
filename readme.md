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

### Schematics

Links to the schematics can be found [here](https://oshwlab.com/adasneves127/alexcomputer)

## Schematics Design Rational & Rules

### Data bus

- Each board, which connects to the data bus, will have 2 connectors for such bus. Both connectors will be 1 pin by 10 pins.

- On all boards, with the exception of the control board, the connectors will be of the following types. One male, and one female. On the control board, the connectors will both be female.

- The rational behind this idea is such that the data lines can be daisy chained together, without the need for crazy long cables. Also, by following the male connectors, you will always find your way to the control board.

- The memory board will also have 2 male, as well as 2 female connectors. One male will connect to the PC/SP/IR/F board, while the other will connect to the video card. The other 2 ports are designed for future use.
  
### Address Bus

- Each board, which connects to the address bus, will have a 2 pin by 10 pin connector.

- The PC/SP/IR/F Board, as well as the memory board will have 2 address connectors.

- The dual connectors on the PC/SP/IR/F Board will be one male, and one female. The PC/SP/IR/F board will be able to modify the address as the program chooses.

- The dual connectors on the Memory board will be both female. One will connect to the PC/SP/IR/F board, while the other will connect to the video board.

### "Instruction" Bus

- The "Instruction" Bus serves 1 real purpose. It connects the Control Unit to the Datapath Controller, as well as the PC/S/IR/F Board. It is comprised of a 1x10 connector.

- The Control Unit will have 2 female connectors, while the PC/SP/IR/F and Datapath Controller boards will have 1 male connector each.

### Keyboard & IO

- The keyboard is a standard PS/2 Connector. It is connected to a PS/2 to TTL Decoder circuit. This circuit outputs it's data to the "I/O" board.
- The I/O Board's main goal is to accept keyboard inputs, latch it's data, and clear the TTL decoder. It's secondary goal is to accept data from the Control Unit, and make it accessible to the GPIO Lines of the card.
- When a key is ready for reaing, it sets the "Interupt" pin high, to signify to the cpu that there is data to be read and processed.

## Assembler

To use the assembler, run the script as python3, and supply an input file.

ex: python3 DALAssembler.py \<-o outputFile> inputFile

## Simulator

To run the simulator, first off, compile it the included shell file.

sh build.sh

After that, run it with ./Sim \<input file\>

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

      - File 3: DAL.txt
        - This file will show the machine code in direct text.
  
#### Language

- Added New Branching Commands

#### Files

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

- Simulator Prototype built in Java
  - System Monitor graphical Display Designed
- Simulator Language changed to Changelog

## [V1.6.2]

### Added

- Added more instructions to the assembler
- Added Changed changelog to ReadMe.md

## [V2.0]

### Added

- Added instructions to the assembler

### Changed

- Simulator changed from C to C++

## [V2.0.1]

### Added

- Added all instructions to the simulator

### Changed

- Changed Memory Map values.

### Removed

- Removed MJB and MBJ instructions, as they were inneficient due to the change in memory layout.

## [V2.1]

### Changed

- Rewrote assembler to be more efficient and intuitive.


### 5/19/22

- Reorganized Repo
  - Added Hardware and Software folders, and sorted into those 2 categories.
- Added our instructions for the Datapath Controller