#pragma once

class Mem{
    /* Important Memory Addresses:
     Memory Map:
        0x0100 - 0x01FF: Stack (0x0100 is bottom of stack)
    */
    public:
       
        Mem();
        unsigned char read(unsigned short address);
       
        void write(unsigned char value, unsigned short address);
    private:
        unsigned char memPageA;
        unsigned char memPageB;
        unsigned char mem[0xFF00];
        unsigned char pagedMem[0xFF][0xFF][0xFF];
};