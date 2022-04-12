import java.util.Scanner;
import java.io.File;

public class Simulator  {
    private static Memory mem;
    public static Registers reg;
    private static ALU alu;
    private static Scanner fileIn = null;
    Simulator(String FileToRun) throws ValueOutOfRangeException{
        try{
            fileIn = new Scanner(new File(FileToRun));
        }
        catch (Exception e){
            System.out.println("Error: File Not Found");
            System.exit(1);
        }

        mem = new Memory();
        reg = new Registers();
        alu = new ALU();
    }

    protected static void loadFile(){
        while(fileIn.hasNextByte()){
            mem.write(fileIn.nextByte());
        }
        
    }

    public static void start(boolean isTextMode){
        loadFile();
    }

    public static void dumpMem(){
        for(int i = 0; i < 65326; i++){
            
            System.out.print(mem.read(i) + " ");
                //mem.incrementAddress();
            if(i % 16 == 0){
                System.out.println();
            }
        }
    }

    public static void load(Register register, int MemoryAddress) throws ValueOutOfRangeException{
        if(MemoryAddress > 255 || MemoryAddress < 0)
            throw new ValueOutOfRangeException("Memory Address must be between 0 and 255");
        register.setValue(mem.read(MemoryAddress));
    }

    public void Fetch(){
        int currIns = mem.read();

        if(currIns >> 4 == 0xA || currIns >> 4 == 0xB){
            currIns = (currIns << 8) | mem.read();
        } else if(currIns >> 4 == 0xC){
            if((currIns & 0b100) == 0b100){
                currIns = (currIns << 8) | mem.read();
            }
            else {
                currIns = (currIns << 16) | (mem.read() << 8) | mem.read();
            }
        } else if(currIns >> 4 == 0xE){
            currIns = (currIns << 8) | mem.read();
        } else if(currIns >> 4 == 0x3){
            currIns = (currIns << 16) | (mem.read() << 8) | mem.read();
        } else if(currIns >> 4 == 0x8){
            if((currIns & 0xF) != 0xC){
                currIns = (currIns << 16) | (mem.read() << 8) | mem.read();
            }
            currIns = (currIns << 16) | (mem.read() << 8) | mem.read();
        }
        Decode(currIns);
    }

    public void Decode(int instruction){
        
        
        //Execute(ins, R1, R2, Data, MemAddress);
    }
    
    public void Execute(String ins, Register R1, Register R2, int Data, int MemAddress) throws ValueOutOfRangeException {
        switch(ins){
            case "ADD":
                alu.ADD(R1, R2);
        }
        Store();
    }

    public void Store(){
        
        Fetch();
    }

}
