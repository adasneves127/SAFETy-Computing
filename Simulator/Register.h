#pragma once

class Register{

    public:
        Register();
        
        void set(unsigned char value);
        void set(unsigned short value);
        unsigned char get();
        void setType(bool type);
        bool getType();
    private:
        unsigned char value8;
        unsigned char value16;
        bool dataLen;
};