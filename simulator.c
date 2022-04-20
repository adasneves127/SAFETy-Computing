#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/* -------------------------------------------------------------------------- */
/*                             Function Prototypes                            */
/* -------------------------------------------------------------------------- */

void writeToMemoryAddr(int address, unsigned char value);
void writeToMemoryPC(unsigned char value);


/* ---------------------------- Global variables ---------------------------- */
unsigned char a, b, x, y, sp, pc;
unsigned char memory[0xFFFF];


int main(int argc , char *argv[]) {

	
    FILE* f=fopen(argv[1],"r");
	
	int i=0;
	//Fill memory with 0xFF (BRK)
	for(i=0; i<0xFFFF; i++)
		memory[i]=0xff;
	i=0;

	//Fill memory with the program
	//This gives a bus error... I don't understand why.
	
	while(!feof(f) && i<=0xFFFF)
	{
		
		int c;
		fscanf(f,"%x\n",&c);
		
		
		unsigned char readIn = (unsigned char)(c & 0xff);
		memory[i] = readIn;
		printf("%x\n",memory[i]);
        i++;
	
	}

	fclose(f);
	return 0;
	
	
}
