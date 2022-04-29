#ifndef REGISTERS_H // include guard
    #define REGISTERS_H
#endif

#include "Register.h"

class Registers{
    public:
        Register A, B, X, Y, SP, INS, PC;
        //Flags: CNZVI
        unsigned char flags;
        void reset();
};