#pragma once

class Mem{
    /* Important Memory Addresses:
     Memory Map:
        0x0100 - 0x01FF: Stack (0x0100 is bottom of stack)
    */
    public:
        unsigned char mem[0xFFFF];
        Mem();
        unsigned char read();
        unsigned char read(unsigned short address);
        void write(unsigned char value);
        void write(unsigned char value, unsigned short address);
};