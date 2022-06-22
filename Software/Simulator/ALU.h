#pragma once
#include "Register.h"

class ALU{
    public:
        unsigned char flags;
        void updateFlags(unsigned char flags);
        ALU(unsigned char flags);
        
        unsigned char ADD(Register r1, Register r2);
        unsigned char SUB(Register r1, Register r2);
        unsigned char CMP(Register r1, Register r2);
        unsigned char INC(Register r1);
        unsigned char DEC(Register r1);
        unsigned char NAND(Register r1, Register r2);


        unsigned char ADD(Register r1, unsigned char val);
        unsigned char SUB(Register r1, unsigned char val);
        unsigned char CMP(Register r1, unsigned char val);
        unsigned char INC(unsigned short address, unsigned char mem[]);
        unsigned char DEC(unsigned short address, unsigned char mem[]);
        void reset();
};