/* 
    Issues to try to understand:
        0xF7 != 247 ?
            In theory it should, as 0xF7 is the hex value of 247 right?
            In reality it doesn't...
*/

#pragma region Includes
#include <stdio.h>
#include <cstdio>
#include <iostream>
#include <string>
#include <string.h>
#include "Registers.h"
#include "Register.h"
#include "ALU.h"
#include "Memory.h"
#pragma endregion

#ifdef __cplusplus__

  #include <iostream>
  #include <string>

  void ClearScreen()
    {
    std::cout << string( 100, '\n' );
    }

#else

  #include <stdio.h>

  void ClearScreen()
    {
    int n;
    for (n = 0; n < 10; n++)
      printf( "\n\n\n\n\n\n\n\n\n\n" );
    }

#endif 

#pragma region Global Variables
Registers reg;
ALU alu(reg.flags);
Mem mem;
bool halted = false;

Register regs[] = {reg.A, reg.B, reg.X, reg.Y};
char regNames[] = "abcd";

bool debug = false;
bool inBreak = false;

#pragma endregion

#pragma region Function Prototypes 
void doInstruction();
int *decode(unsigned char ins);
void readFile(char *argv[]);
unsigned char readMemIncPC();
void push(unsigned char Data);
unsigned char pop();
void graphicsDraw();
void drawToScreen(char line[]);
void printDebug();

#pragma endregion

int main(int argc, char* argv[]){

    if(argc == 2){
        if(*argv[0] == 'd'){
            debug = true;
        }
    }

    //Initialize Registers to be the correct size.
    reg.A.setType(true);
    reg.B.setType(true);
    reg.X.setType(true);
    reg.Y.setType(true);
    reg.SP.setType(true);
    reg.INS.setType(true);
    reg.PC.setType(false);

    if(argc > 1){
        readFile(argv);
    }
    else{
        std::cout << "No file specified!" << std::endl;
        return 0;
    }

    while(!halted && (reg.PC.get() <= 65535)){
        doInstruction();
        if(debug){
            printDebug();
        }
    }

}

void printDebug(){
    std::cout << "Debug Info: " << std::endl;;
    for(int i = 0; i < 4; i++){
        std::cout << regNames[i] << ": " << regs[i].get() << ", ";
    }
    std::cout << std::endl;

    std::cout << "Flags: " << alu.flags << std::endl;

    std::cout << "PC: " << reg.PC.get() << std::endl;
    std::cout << "INS: " << reg.INS.get() << std::endl;
    std::cout << "SP: " << reg.SP.get() << std::endl << std::endl;
}

void readFile(char *argv[]){
    FILE* f=fopen(argv[1],"r");
	
	int i=0;
	//Fill memory with 0xFF (BRK)
	for(i=0; i<0xFFFF; i++)
		mem.write(0x00, i);
	i=0x8000;

	
	
	while(!feof(f) && i<=0xFFFF)
	{
		int c;
		fscanf(f,"%x\n",&c);
		
		unsigned char readIn = (unsigned char)(c & 0xff);
		mem.write(readIn, i);
		//printf("%x\n",mem.mem[i]);
        i++;
	}

	fclose(f);

    char line[] = {"Hello!"};
    drawToScreen(line);

}

void doInstruction(){
    
    // Get the instruction
    // Get the opcode
    // Get the operands
    // Get the flags
    // Get the address
    // Get the memory
    // Execute the instruction

    alu.updateFlags(reg.flags);
    reg.INS.set(mem.read(reg.PC.get()));
    reg.PC.set((unsigned short)(reg.PC.get() + 1));

    

    unsigned char ins = reg.INS.get();
    Register RD = regs[(ins >> 2) & 0x3];
    Register RS = regs[(ins) & 0x3];
    switch(ins){
        case 0x00:
            //NOP
            break;
        case 0x01:
            //RST
            reset();
            break;
        case 0x02:
            halted = true;
            break;
        case 0x03:
            //BRK
            inBreak = true;
            break;
        case 0x04:
            //RST
            inBreak = false;
            break;
        case 0x05:
            alu.flags &= 0b01111111;
            break;
        case 0x06:
            alu.flags &= 0b10111111;
            break;
        case 0x07:
            alu.flags &= 0b11011111;
            break;
        case 0x08:
            alu.flags &= 0b11101111;
            break;
        case 0x09:
            alu.flags &= 0b11110111;
            break;
        case 0x10:
        case 0x14:
        case 0x18:
        case 0x1c:
            //LSL
            RD.set((unsigned char)(RD.get() << 1));
            break;
        case 0x11:
        case 0x15:
        case 0x19:
        case 0x1d:
            //LSR
            RD.set((unsigned char)(RD.get() >> 1));
            break;
        case 0x12:
        case 0x16:
        case 0x1a:
        case 0x1e:
            //ADD IMM
            alu.ADD(RD, (unsigned char)readMemIncPC());
            break;
        case 0x13:
        case 0x17:
        case 0x1b:
        case 0x1f:
            //SUB IMM
            alu.SUB(RD, (unsigned char)readMemIncPC());
            break;
        case 0x20:
        case 0x24:
        case 0x28:
        case 0x2c:
            //INC
            alu.ADD(RD, 1);
            break;
        case 0x21:
        case 0x25:
        case 0x29:
        case 0x2d:
            //DEC
            alu.SUB(RD, 1);
            break;
        case 0x30:
        case 0x34:
        case 0x38:
        case 0x3c:
            //POP
            RD.set(pop());
            break;
        case 0x61:
        case 0x62:
        case 0x63:
        case 0x64:
        case 0x66:
        case 0x67:
        case 0x68:
        case 0x69:
        case 0x6b:
        case 0x6c:
        case 0x6d:
        case 0x6e:
            //TRANSFER
            RD.set(RS.get());
            break;
        case 0x70:
            //JMP
            reg.PC.set((unsigned short)(readMemIncPC() << 8 | readMemIncPC()));
            break;
        case 0x71:
            //JSR
            push((unsigned char)(reg.PC.get() >> 8));
            push((unsigned char)(reg.PC.get() & 0xFF));
            reg.PC.set((unsigned short)(readMemIncPC() << 8 | readMemIncPC()));
            break;
        case 0x72:
            //RET
            reg.PC.set((unsigned short)(pop() | (pop() << 8)));
            break;
        case 0x73:
            //JSE
            if(alu.flags & 0b10000000){
                push((unsigned char)(reg.PC.get() >> 8));
                push((unsigned char)(reg.PC.get() & 0xFF));
                reg.PC.set((unsigned short)(readMemIncPC() << 8 | readMemIncPC()));
            }
            break;
        case 0x74:
            //JSN
            if((alu.flags & 0b01000000)){
                push((unsigned char)(reg.PC.get() >> 8));
                push((unsigned char)(reg.PC.get() & 0xFF));
                reg.PC.set((unsigned short)(readMemIncPC() << 8 | readMemIncPC()));
            }
            break;
        case 0x75:
            //JSL
            if(alu.flags & 0b10000000){
                reg.PC.set((unsigned short)(readMemIncPC() << 8 | readMemIncPC()));
            }
            break;
        case 0x76:
            //BEQ
            if(!(alu.flags & 0b01000000)){
                push((unsigned char)(reg.PC.get() >> 8));
            }
            break;
        case 0x80:
        case 0x81:
        case 0x82:
        case 0x83:
        case 0x84:
        case 0x85:
        case 0x86:
        case 0x87:
        case 0x88:
        case 0x89:
        case 0x8a:
        case 0x8b:
        case 0x8c:
        case 0x8d:
        case 0x8e:
        case 0x8f:
            alu.ADD(RD, RS);
            break;

        case 0x90:
        case 0x91:
        case 0x92:
        case 0x93:
        case 0x94:
        case 0x95:
        case 0x96:
        case 0x97:
        case 0x98:
        case 0x99:
        case 0x9a:
        case 0x9b:
        case 0x9c:
        case 0x9d:
        case 0x9e:
        case 0x9f:
            alu.SUB(RD, RS);
            break;

        case 0xa0:
        case 0xa1:
        case 0xa2:
        case 0xa3:
        case 0xa4:
        case 0xa5:
        case 0xa6:
        case 0xa7:
        case 0xa8:
        case 0xa9:
        case 0xaa:
        case 0xab:
        case 0xac:
        case 0xad:
        case 0xae:
        case 0xaf:
            alu.SUB(RD, RS);
            break;
        
    }

    //halted = true;
}

// Reset the system
void reset(){
    reg.reset();
    halted = false;
}

// Push to the stack, and increment SP
void push(unsigned char Data){
    mem.write(Data, 0x100 + reg.SP.get());
    reg.SP.set((unsigned char)(reg.SP.get() + 1));
}

// Pop from the stack, and decrement SP. Returns the popped value
unsigned char pop(){
    reg.SP.set((unsigned short)(reg.SP.get() - 1));
    unsigned char Data = mem.read(reg.SP.get() + 100);
    return Data;
    
}

// Reads the byte at the current PC and increments the PC. Returns the byte
unsigned char readMemIncPC(){
    unsigned char data = mem.read(reg.PC.get());
    reg.PC.set((unsigned short)(reg.PC.get() + 1));
    return data;
}

void graphicsMove(){
    //If we have drawn more than 24 lines, then we need to shift the screen up
    for(int i = 1; i < 24; i++){
        for(int j = 0; j < 40; j++){
            //Copy the current line to the previous line
            mem.write(mem.read(0x200 + (i * 24) + j), 0x200 + ((i-1) * 24) + j);
        }
    }
}


void graphicsDraw(){
    //Clear the screen
    ClearScreen();

    //Draw the screen
    //Bounding top
    std::cout << "|";
    for(int i = 0; i < 40; i++){
        std::cout << "-";
    }

    std::cout << "|" << std::endl;

    //Draw from screen mem
    for(int i = 0; i < 24; i++){
        std::cout << "|";
        for(int j = 0; j < 40; j++){
            unsigned char character = mem.read(0x200 + (i * 24) + j);
            if(character == 0x00){
                std::cout << " ";
            } else{
                std::cout << character;
            }
        }
        std::cout << "|" << std::endl;
    }

    //Bounding bottom
    std::cout << "|";
    for(int i = 0; i < 40; i++){
        std::cout << "-";
    }
    std::cout << "|" << std::endl;
}

//Call this function to draw to the screen
void drawToScreen(char line[]){

    //Get the mem offset
    unsigned char memOffset = mem.read(0x5E9);

    //Get the length of the string
    int strlength = strlen(line);

    //Split the string into lines
    char portions[24][40];
    int count = 0;

    //While the portions do not contain all of the string
    if(count * 40 <= strlength){
        //Split the string into portions
        memcpy(portions[count], line + (count * 40), 40);
    }
        
    //Copy the portions of the string into VidMem
    for(int i = 0; i < count; i++){
        for(int j = 0; j < 40; j++){
            mem.write(portions[i][j], 0x200 + (i * count) + j);
        }
    }
    //Increment the mem offset
    mem.write((unsigned char)(mem.read(0x5E9) + count + 1), 0x5E9);
    if(mem.read(0x5E9) > 24){
        mem.write(0x5E9, 24);
    }
    //If we have drawn 24 lines to the screen, move the screen.
    if(mem.read(0x5E9) >= 24){
        graphicsMove();
    }
    //Draw the screen
    graphicsDraw();
}