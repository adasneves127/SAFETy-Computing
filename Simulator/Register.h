#pragma once

class Register{

    public:
        Register();
        
        void set(unsigned char value);
        void set(unsigned short value);
        unsigned short get();
        void setType(bool type);
        bool getType();
    private:
        unsigned char value8;
        unsigned short value16;
        bool dataLen;
};