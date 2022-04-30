#include <stdio.h>
#include <cstdio>
#include <iostream>
#include <string>
#include "Registers.h"
#include "Register.h"
#include "ALU.h"
#include "Memory.h"

#ifdef __cplusplus__

  #include <iostream>
  #include <string>

  void ClearScreen()
    {
    cout << string( 100, '\n' );
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

Registers reg;
ALU alu(reg.flags);
Mem mem;
bool halted = false;

Register regs[] = {reg.A, reg.B, reg.X, reg.Y};

void doInstruction();
int *decode(unsigned char ins);
void readFile(char *argv[]);
unsigned char readMemIncPC();
void push(unsigned char Data);
unsigned char pop();
void graphicsDraw();

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

    while(!halted){
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

	//Fill memory with the program
	//This gives a bus error... I don't understand why.
	
	while(!feof(f) && i<=0xFFFF)
	{
		int c;
		fscanf(f,"%x\n",&c);
		
		unsigned char readIn = (unsigned char)(c & 0xff);
		mem.mem[i] = readIn;
		printf("%x\n",mem.mem[i]);
        i++;
	
	}

	fclose(f);

}

void doInstruction(){
    graphicsDraw();
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

    if(ins == 0xA0){ //Add 2 Registers
        unsigned char nextIns = mem.read(reg.PC.get());
        reg.PC.set((unsigned short)(reg.PC.get() + 1));
        //TODO: Finish Command

    } else if((ins & 0b11111100) == 0b10101000){ //Registers Addition
        // ADD
        
    } else if(ins == 0xF9){ //HLT
        halted = true;
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
    } else if(ins == 0x25){ //CLC
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
    }

    halted = true;
}


void reset(){
    reg.reset();
}

void push(unsigned char Data){
    mem.mem[reg.SP.get() + 0x100] = Data;
    reg.SP.set((unsigned char)(reg.SP.get() + 1));
}

unsigned char pop(){
    reg.SP.set((unsigned short)(reg.SP.get() - 1));
    unsigned char Data = mem.mem[reg.SP.get() + 100];
    mem.mem[reg.SP.get() + 0x100] = 0x00;
    return Data;
}

unsigned char readMemIncPC(){
    unsigned char data = mem.read(reg.PC.get());
    reg.PC.set((unsigned short)(reg.PC.get() + 1));
    return data;
}


void graphicsDraw(){
    ClearScreen();
    for(int i = 0; i < 24; i++){
        for(int j = 0; j < 20; j++){
            unsigned char character = mem.read(0x200 + (i * 24) + j);
            if(character == 0x00){
                std::cout << " ";
            } else{
                std::cout << character;
            }
        }
        std::cout << std::endl;
    }
}


