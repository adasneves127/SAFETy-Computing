import java.util.Arrays;

public class Main {
    public static Simulator sim;
    public static void main(String[] args) throws ValueOutOfRangeException {
        if(args.length == 0) {
            System.out.println("Error: No File Specified");
            System.out.println("Usage: java Main <file> [t, d]");
            System.exit(1);
        }

        if(Arrays.asList(args).contains("-h")) {
            System.out.println("Dasneves Assembly Simulator");
            System.out.println("v 1.0");
            System.out.println("Usage: java Main <file> [t, d]");
            System.out.println("t: Starts the simulator in text mode");
            System.out.println("d: Starts the simulator in data mode");
            System.exit(0);
        }
        
        String filePath = args[0];

        sim = new Simulator(filePath);

        SystemMon monitor = new SystemMon();
        Thread thread = new Thread(monitor);
        thread.start();

        if(args.length == 2){
            if(args[1].equals("t")) {
                Simulator.start(true);
            } else if(args[1].equals("d")) {
                Simulator.start(false);
            } else {
                System.out.println("Error: Invalid Argument");
            }
        }

    }
}
