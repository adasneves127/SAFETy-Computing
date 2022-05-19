#pragma once

#include "Register.h"

class Registers{
    public:
        Register A, B, X, Y, SP, INS, PC;
        //Flags: CNZVI000
        unsigned char flags;
        void reset();
};