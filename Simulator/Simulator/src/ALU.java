public class ALU {

    public ALU(){

    }

    //All ALU Operations take place in the A and B Registers
    public void ADD(Register A,  Register B) throws ValueOutOfRangeException{
        Simulator.reg.stack.push(Simulator.reg.B.getValue());
        A.Transfer(Simulator.reg.A);
        B.Transfer(Simulator.reg.B);
        Simulator.reg.A.setValue((Simulator.reg.A.getValue() + Simulator.reg.B.getValue()));
        Simulator.reg.B.setValue(Simulator.reg.stack.pop());
    }

    public void SUB(Register A, Register B) throws ValueOutOfRangeException{
        Simulator.reg.stack.push(Simulator.reg.B.getValue());
        Simulator.reg.stack.push(Simulator.reg.A.getValue());
        Simulator.reg.B.Transfer(Simulator.reg.A);
        Simulator.reg.B.setValue(0xFF);
        XOR(Simulator.reg.A, Simulator.reg.B);
        Simulator.reg.B.setValue(1);
        ADD(Simulator.reg.A, Simulator.reg.B);
        Simulator.reg.A.Transfer(Simulator.reg.B);

        Simulator.reg.A.setValue(Simulator.reg.stack.pop());
        ADD(A, B);

        Simulator.reg.B.setValue(Simulator.reg.stack.pop());
    }

    public void XOR(Register A, Register B) throws ValueOutOfRangeException{
        Simulator.reg.push(Simulator.reg.B.getValue());
        A.setValue((A.getValue() ^ B.getValue()));
        Simulator.reg.B.setValue(Simulator.reg.pop());
    }

    public void AND(Register A, Register B) throws ValueOutOfRangeException{
        Simulator.reg.push(Simulator.reg.B.getValue());
        B.Transfer(Simulator.reg.B);
        A.Transfer(Simulator.reg.A);

        Simulator.reg.A.setValue((Simulator.reg.A.getValue() & Simulator.reg.B.getValue()));

        Simulator.reg.B.setValue(Simulator.reg.pop());
    }

    public void NAND(Register A, Register B) throws ValueOutOfRangeException{
        Simulator.reg.push(Simulator.reg.B.getValue());
        B.Transfer(Simulator.reg.B);
        A.Transfer(Simulator.reg.A);
        Simulator.reg.A.setValue(~(Simulator.reg.A.getValue() & Simulator.reg.B.getValue()));
        Simulator.reg.B.setValue(Simulator.reg.pop());
    }



}
