CC = clang++

CFLAGS = -I.

Main: Main.o ALU.o Register.o Memory.o Registers.o
	$(CC) $(CFLAGS) -o Simulator Main.o ALU.o Register.o Memory.o Registers.o
	rm -f ./*.o 

ALU.o: ALU.cpp ALU.h
	$(CC) $(CFLAGS) -c ALU.cpp

Register.o: Register.cpp Register.h
	$(CC) $(CFLAGS) -c Register.cpp

Registers.o: Registers.cpp Registers.h
	$(CC) $(CFLAGS) -c Registers.cpp

Memory.o: Memory.cpp Memory.h
	$(CC) $(CFLAGS) -c Memory.cpp
