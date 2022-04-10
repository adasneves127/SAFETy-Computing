import java.util.Scanner;
import java.io.File;

public class Simulator {
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
        for(int i = 0; i < 256; i++){
            for(int j = 0; j < 256; j++){

                System.out.print(mem.read(j) + " ");
                //mem.incrementAddress();
            }
            mem.IMP();
            System.out.println();
        }
    }

    public static void load(Register register, int MemoryAddress) throws ValueOutOfRangeException{
        if(MemoryAddress > 255 || MemoryAddress < 0)
            throw new ValueOutOfRangeException("Memory Address must be between 0 and 255");
        register.setValue(mem.read(MemoryAddress));
    }

    public void Fetch(){
        
    }

    public void Decode(){
        
    }
    
    public void Execute(){
        
    }

    public void Store(){
        
    }

}
