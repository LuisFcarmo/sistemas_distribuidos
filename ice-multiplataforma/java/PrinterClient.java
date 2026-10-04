import com.zeroc.Ice.Communicator;
import com.zeroc.Ice.ObjectPrx;
import com.zeroc.Ice.Util;

public class PrinterClient {

    public static void main(String[] args) {
        String host = "127.0.0.1";
        int port = 11000;
        if (args.length > 0 && !args[0].startsWith("-")) {
            host = args[0];
        }
        if (args.length > 1 && args[1].matches("\\d+")) {
            port = Integer.parseInt(args[1]);
        }

        int status = 0;
        try (Communicator communicator = Util.initialize(args)) {
            ObjectPrx base = communicator.stringToProxy("SimplePrinter:tcp -h " + host + " -p " + port);
            Demo.PrinterPrx printer = Demo.PrinterPrx.checkedCast(base);
            if (printer == null) {
                throw new RuntimeException("Proxy invalido");
            }

            System.out.println("printString:  " + printer.printString("Hello World!"));
            System.out.println("toUpper:      " + printer.toUpper("sistemas distribuidos"));
            System.out.println("add:          " + printer.add(35, 7));
            System.out.println("repeatString: " + printer.repeatString("ZeroC-Ice", 3));
        } catch (Exception e) {
            System.out.println("Erro: " + e);
            status = 1;
        }
        System.exit(status);
    }
}
