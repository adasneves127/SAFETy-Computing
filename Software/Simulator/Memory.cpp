#include "Memory.h"

Mem::Mem(){

}

unsigned char Mem::read(unsigned short address){
    return mem[address];
}

void Mem::write(unsigned char value, unsigned short address){
    mem[address] = value;
}