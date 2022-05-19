#include "Registers.h"
#include "Register.h"

void Registers::reset(){
     A.set((unsigned char)0);
     B.set((unsigned char)0);
     X.set((unsigned char)0);
     Y.set((unsigned char)0);
    SP.set((unsigned char)0);
   INS.set((unsigned char)0);
    PC.set((unsigned short)0);
}