#include "ALU.h"
#include "Registers.h"
#include "Memory.h"
#include "Register.h"

unsigned char flags = 0;

void checkFlags(unsigned char result){
    if(result == 0){
        flags = flags | 0b0;
    }
}

ALU::ALU(unsigned char flags){
    this->flags = flags;
}

void ALU::updateFlags(unsigned char flags){
    this->flags = flags;
}


unsigned char ALU::ADD(Register r1, Register r2){
    r1.set((unsigned char)(r1.get() + r2.get()));
    return flags;
}

unsigned char ALU::ADD(Register r1, unsigned char val){
    r1.set((unsigned char)(r1.get() + val));
    return flags;
}

unsigned char ALU::SUB(Register r1, Register r2){
    r1.set((unsigned char)(r1.get() - r2.get()));
    return flags;
}

unsigned char ALU::SUB(Register r1, unsigned char val){
    r1.set((unsigned char)(r1.get() - val));
    return flags;
}

unsigned char ALU::CMP(Register r1, Register r2){
    if(r1.get() == r2.get()){
        return true;
    }
    else{
        return false;
    }
}

unsigned char ALU::CMP(Register r1, unsigned char val){
    if(r1.get() == val){
        return true;
    }
    else{
        return false;
    }
}

unsigned char ALU::INC(Register r1){
    if(r1.getType()){
        r1.set((unsigned char)(r1.get() + 1));
    } else{
        r1.set((unsigned short)(r1.get() + 1));
    }

    return flags;
}

unsigned char ALU::INC(unsigned short address, unsigned char mem[]){
    mem[address] = mem[address] + 1;
    return flags;
}

unsigned char ALU::DEC(Register r1){
    if(r1.getType()){
        r1.set((unsigned char)(r1.get() - 1));
    } else{
        r1.set((unsigned short)(r1.get() - 1));
    }

    return flags;
}

unsigned char ALU::DEC(unsigned short address, unsigned char mem[]){
    mem[address] = mem[address] - 1;
    return flags;
}