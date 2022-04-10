public class Memory {
    private int memPage = 0;
    private int memAddress = 0;
    private int[][] memory = null;
    public Memory(){
        memPage = 0;
        memAddress = 0;
        memory = new int[256][256];
    }
    
    public String getAddress(){
        return Integer.toHexString(memPage << 8) + Integer.toHexString(memAddress);
    }

    public void incrementAddress(){
        memAddress++;
    }

    public void write(int data) throws IllegalArgumentException{
        if(data > 255 || data < 0)
            throw new IllegalArgumentException("Data must be between 0 and 255");
        memory[memPage][memAddress] = data;
        incrementAddress();
    }

    public int read(){
        return memory[memPage][memAddress];
    }

    public int read(int address) throws IllegalArgumentException{
        if(address > 255 || address < 0)
            throw new IllegalArgumentException("Address must be between 0 and 255");
        return memory[memPage][address];
    }

    public void IMP(){
        memPage++;
    }

    public void DEC(){
        memPage--;
    }

    public void IPJ(int difference, int address){

    }

    public void jmp(int address){
        memAddress = (byte)address;
    }

}
