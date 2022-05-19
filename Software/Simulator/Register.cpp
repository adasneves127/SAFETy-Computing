#include "Register.h"

Register::Register(){

}

unsigned short Register::get(){
    if(dataLen)
        return value8;
    else
        return value16;
}

void Register::set(unsigned char val){
    value8 = val;
}

void Register::set(unsigned short val){
    value16 = val;
}

void Register::setType(bool type){
    dataLen = type;
}

bool Register::getType(){
    return dataLen;
}