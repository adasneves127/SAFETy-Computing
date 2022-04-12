public class Memory {
    private int memAddress = 0;
    private int[] memory = null;
    public Memory(){
        memAddress = 0;
        memory = new int[65325];
    }
    
    public String getAddress(){
        return Integer.toHexString(memAddress);
    }

    public void incrementAddress(){
        memAddress++;
    }

    public void write(int data) throws IllegalArgumentException{
        if(data > Math.pow(2, 8) || data < 0)
            throw new IllegalArgumentException("Data must be between 0 and 255");
        memory[memAddress] = data;
        System.out.println(data);
        incrementAddress();
    }

    public void write(int data, int address) throws IllegalArgumentException{
        if(data > Math.pow(2, 8) || data < 0)
            throw new IllegalArgumentException("Data must be between 0 and 255");
        else if (address > memory.length || address < 0)
            throw new IllegalArgumentException("Address must be between 0 and " + memory.length);
        memory[address] = data;
    }

    public int read(){
        int retVal = memory[memAddress];
        incrementAddress();
        return retVal;
    }

    public int read(int address) throws IllegalArgumentException{
        if(address > memory.length || address < 0)
            throw new IllegalArgumentException("Address must be between 0 and 255");
        return memory[address];
    }

    public void setAddress(int address){
        memAddress = address;
    }


}
