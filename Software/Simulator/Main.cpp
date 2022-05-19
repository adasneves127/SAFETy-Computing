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
#pragma endregion

int main(int argc, char* argv[]){
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
        return 0;
    }

    while(!halted && (reg.PC.get() <= 65535)){
        doInstruction();
    }

}

void readFile(char *argv[]){
    FILE* f=fopen(argv[1],"r");
	
	int i=0;
	//Fill memory with 0xFF (BRK)
	for(i=0; i<0xFFFF; i++)
		mem.mem[i]=0x00;
	i=0;

	
	
	while(!feof(f) && i<=0xFFFF)
	{
		int c;
		fscanf(f,"%x\n",&c);
		
		unsigned char readIn = (unsigned char)(c & 0xff);
		mem.mem[i] = readIn;
		//printf("%x\n",mem.mem[i]);
        i++;
	}

	fclose(f);

    char line[] = {"Hello!"};
    drawToScreen(line);

}

void doInstruction(){
    std::cout << "PC: " << reg.PC.get() << std::endl;
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
    std::cout << "INS: " << (int)ins << std::endl;

    if(ins == 0xA0){ //Add 2 Registers
        unsigned char nextIns = readMemIncPC();
        unsigned char R1 = nextIns >> 6;
        unsigned char R2 = (nextIns & 0xF) >> 2;
        reg.flags = alu.ADD(regs[R1], regs[R2]);

    } else if((ins & 0b11111100) == 0b10101000){ //Registers Addition
        // ADD
        unsigned char reg1 = (ins & 0b00000011);
        unsigned char data = readMemIncPC();
        reg.flags = (alu.ADD(regs[reg1], data));
        
    } else if(ins == 0xF7){ //HLT
        halted = true;
        std::cout << "HALT" << std::endl;
    } else if (ins == 0xC1){ // Push
        push(regs[mem.read(reg.PC.get()) >> 6].get());
        reg.PC.set((unsigned char)(reg.PC.get() + 1));
    } else if (ins == 0xC2){ // Pop
        unsigned char RegData = mem.read(reg.PC.get()) >> 6;
        regs[RegData].set(pop());
    } else if ((ins & 0b11111100) == 0b01010100){ // LSR
        regs[ins & 0b11].set((unsigned short)(regs[ins & 0b11].get() >> 1));
    } else if ((ins & 0b11111100) == 0b01010000){ // LSL
        regs[ins & 0b11].set((unsigned char)(regs[ins & 0b11].get() << 1));
    } else if (ins == 0x8C){ // RET
        unsigned char UN = pop(); // Get the high byte
        unsigned char LN = pop(); // Get the low byte
        unsigned short addr = (UN << 8) | LN; // Combine the bytes
        reg.PC.set(addr); // Set the PC
    } else if (ins == 0x70){ // JMP
        unsigned char LN = readMemIncPC(); // Get the low byte
        unsigned char UN = readMemIncPC(); // Get the high byte
        unsigned short addr = (UN << 8) | LN; // Combine the bytes
        reg.PC.set(addr); // Set the PC
    } else if(ins == 0xA2){ // Increment Register
        unsigned char data = readMemIncPC() >> 6; // Get the register
        reg.flags |= alu.INC(regs[data]); // Increment the register
    } else if(ins == 0xB4){ // Increment Mem Addr
        unsigned char LN = readMemIncPC(); // Get the low byte
        unsigned char UN = readMemIncPC(); // Get the high byte
        unsigned short addr = (UN << 8) | LN; // Combine the bytes
        reg.flags |= alu.INC(addr, mem.mem);
    } else if(ins == 0xB7){ //Register Decrement
        unsigned char data = readMemIncPC() >> 6; // Get the register
        reg.flags |= alu.INC(regs[data]); // Increment the register
    } else if(ins == 0xB8) { // Mem Decrement
        unsigned char LN = readMemIncPC(); // Get the low byte
        unsigned char UN = readMemIncPC(); // Get the high byte
        unsigned short addr = (UN << 8) | LN; // Combine the bytes
        reg.flags |= alu.DEC(addr, mem.mem);
    }else if(ins == 0x25){ //CLC
        reg.flags = reg.flags & 0b01111111;
    } else if(ins == 0x26){ //CLN
        reg.flags = reg.flags & 0b10111111;
    } else if(ins == 0x27){ //CLZ
        reg.flags = reg.flags & 0b11011111;
    } else if(ins == 0x28){ //CLV
        reg.flags = reg.flags & 0b11101111;
    } else if(ins == 0x29){ //CLI
        reg.flags &= 0b11110111;
    } else if(ins == 0x3A){ //SIF
        reg.flags |= 0b00001000;
    } else if(ins == 0x8E){ //JSN
        if((reg.flags & 0b01000000) == 0b10000000){
            unsigned char LN = readMemIncPC(); // Get the low byte
            unsigned char UN = readMemIncPC(); // Get the high byte
            unsigned short addr = (UN << 8) | LN; // Combine the bytes
            push((unsigned char)(reg.PC.get() >> 8));
            push((unsigned char)(reg.PC.get() & 0xFF));
            reg.PC.set(addr); // Set the PC
        }
    } else if(ins == 0x8D){ //JSE
        if((reg.flags & 0b00100000) == 0b00100000){
            unsigned char LN = readMemIncPC(); // Get the low byte
            unsigned char UN = readMemIncPC(); // Get the high byte
            unsigned short addr = (UN << 8) | LN; // Combine the bytes
            push((unsigned char)(reg.PC.get() >> 8));
            push((unsigned char)(reg.PC.get() & 0xFF));
            reg.PC.set(addr); // Set the PC
        }
    } else if(ins == 0x8B){ //JSR
        unsigned char LN = readMemIncPC();
        unsigned char UN = readMemIncPC();
        unsigned short addr = (UN << 8) | LN;
        push((unsigned char)(reg.PC.get() >> 8));
        push((unsigned char)(reg.PC.get() & 0xFF));
        reg.PC.set(addr);
    } else if(ins == 0x31){ //BEQ
        if((reg.flags & 0b00100000) == 0b00100000){
            unsigned char LN = readMemIncPC();
            unsigned char UN = readMemIncPC();
            unsigned short addr = (UN << 8) | LN;
            reg.PC.set(addr);
        }
    } else if(ins == 0x30){ //BNE
        if((reg.flags & 0b01000000) == 0b01000000){
            unsigned char LN = readMemIncPC();
            unsigned char UN = readMemIncPC();
            unsigned short addr = (UN << 8) | LN;
            reg.PC.set(addr);
        }
    } else if((ins & 0xF0) == 0xD0){ // Compare
        unsigned char R1 = (ins & 0b00001100) >> 2;
        unsigned char R2 = (ins & 0b00000011);
        reg.flags |= alu.CMP(regs[R1], regs[R2]);
    } else if((ins & 0b11001100) == 0xCC){ //Store
        unsigned char LN = readMemIncPC();
        unsigned char UN = readMemIncPC();
        unsigned short addr = (UN << 8) | LN;
        mem.write(addr, regs[ins & 0b11].get());
    } else if((ins & 0b11001000) == 0xC8){ // Load from Mem
        unsigned char LN = readMemIncPC();
        unsigned char UN = readMemIncPC();
        unsigned short addr = (UN << 8) | LN;
        regs[ins & 0b11].set(mem.read(addr));
    } else if((ins & 0xC4) == 0xC4){ // Load Imm
        unsigned char data = readMemIncPC();
        regs[ins & 0b11].set(data);
    } else if(ins == 0xC0){
        unsigned char data = readMemIncPC();
        unsigned char R1 = ins >> 6;
        unsigned char R2 = (ins & 0b1100) >> 2;
        regs[R1].set(regs[R2].get());
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
    mem.mem[reg.SP.get() + 0x100] = Data;
    reg.SP.set((unsigned char)(reg.SP.get() + 1));
}

// Pop from the stack, and decrement SP. Returns the popped value
unsigned char pop(){
    reg.SP.set((unsigned short)(reg.SP.get() - 1));
    unsigned char Data = mem.mem[reg.SP.get() + 100];
    mem.mem[reg.SP.get() + 0x100] = 0x00;
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
            mem.mem[0x200 + ((i-1) * 24) + j] = mem.mem[0x200 + (i * 24) + j];
            mem.mem[0x200 + (i * 24) + j] = 0x00;
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
            mem.mem[0x200 + (i * count) + j] = portions[i][j];
        }
    }
    //Increment the mem offset
    mem.mem[0x5E9] = (unsigned char)(mem.read(0x5E9) + count + 1);
    if(mem.read(0x5E9) > 24){
        mem.mem[0x5E9] = 24;
    }
    //If we have drawn 24 lines to the screen, move the screen.
    if(mem.read(0x5E9) >= 24){
        graphicsMove();
    }
    //Draw the screen
    graphicsDraw();
}