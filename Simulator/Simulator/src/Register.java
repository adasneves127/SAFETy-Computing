public class Register {
    protected int value;

    public Register() {
        value = 0;
    }

    public void setValue(int value) throws ValueOutOfRangeException {
        if(value > 255 || value < 0)
            throw new ValueOutOfRangeException("Value must be between 0 and 255");
        this.value = value;
    }

    public int getValue(){
        return this.value;
    }

    public void Transfer(Register to) throws ValueOutOfRangeException{
        to.setValue(this.value);
    }
}
