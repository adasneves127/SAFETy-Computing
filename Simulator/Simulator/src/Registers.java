import java.util.Stack;

public class Registers {
    public Register A, B, X, Y;
    Stack<Integer> stack;
    byte SP, PC;

    boolean[] Flags;
    //Flags[0] = Zero Flag
    //Flags[1] = Carry Flag
    //Flags[2] = Overflow Flag
    //Flags[3] = Interrupt Flag

    public Registers() throws ValueOutOfRangeException{
        A = new Register();
        B = new Register();
        X = new Register();
        Y = new Register();

        A.setValue((byte)0);
        B.setValue((byte)0);
        X.setValue((byte)0);
        Y.setValue((byte)0);
        SP = 0;
        PC = 0;

        Flags = new boolean[4];
        Flags[0] = false;
        Flags[1] = false;
        Flags[2] = false;
        Flags[3] = false;
    }

    public void push(int value) throws ValueOutOfRangeException, StackOverflowError{
        if(value > 255 || value < 0)
            throw new ValueOutOfRangeException("Value must be between 0 and 255");
        if(stack.size() >= 255){
            throw new StackOverflowError("Stack Overflow");
        }
        stack.push(value);
    }

    public int pop(){
        return stack.pop();
    }

    public void load(Register rTL, byte data) throws ValueOutOfRangeException{
        rTL.setValue(data);
    }
}
