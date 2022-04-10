import javax.swing.*;
import javax.swing.table.DefaultTableModel;

public class SystemMon extends JFrame implements Runnable {
    public void run() {
        JFrame frame = new JFrame("System Monitor");
        frame.setSize(1200, 600);
        frame.setVisible(true);

        JScrollPane scroller;

        DefaultTableModel model = new DefaultTableModel(); 
        JTable table = new JTable(model); 

        model.addColumn("Page");
        model.addColumn("Address");
        model.addColumn("Data");
        

        scroller = new JScrollPane(table);
        table.setAutoResizeMode(JTable.AUTO_RESIZE_OFF);
        table.getColumnModel().getColumn(0).setPreferredWidth(50);
        table.getColumnModel().getColumn(1).setPreferredWidth(70);
        table.getColumnModel().getColumn(2).setPreferredWidth(50);

        frame.add(scroller);
        frame.setVisible(true);
        scroller.setVisible(true);
        while(true){
            Main.sim.dumpMem();
        }
    }
}
