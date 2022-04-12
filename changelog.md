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