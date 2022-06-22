#include "Memory.h"

Mem::Mem(){

}

unsigned char Mem::read(unsigned short address){
    if(address < 0xFF00)
        return mem[address];
    else{
        return pagedMem[memPageA][memPageB][address & 0xFF];
    }
}

void Mem::write(unsigned char value, unsigned short address){
    mem[address] = value;

    if(address == (0xFF00 - 1)){
        memPageB = value;
    }
    else if(address == (0xFF00 - 2)){
        memPageA = value;
    }

}

