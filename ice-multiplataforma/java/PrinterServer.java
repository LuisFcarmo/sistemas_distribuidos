import com.zeroc.Ice.Communicator;
import com.zeroc.Ice.Current;
import com.zeroc.Ice.ObjectAdapter;
import com.zeroc.Ice.Util;

import java.util.Collections;

public class PrinterServer {

    static class PrinterI implements Demo.Printer {
        @Override
        public String printString(String s, Current current) {
            System.out.println("printString: " + s);
            return s + "*";
        }

        @Override
        public String toUpper(String s, Current current) {
            System.out.println("toUpper: " + s);
            return s.toUpperCase();
        }

        @Override
        public int add(int a, int b, Current current) {
            System.out.println("add: " + a + " + " + b + " = " + (a + b));
            return a + b;
        }

        @Override
        public String repeatString(String s, int times, Current current) {
            System.out.println("repeatString: " + s + " (" + times + "x)");
            return String.join(" ", Collections.nCopies(times, s));
        }

        @Override
        public void shutdown(Current current) {
            System.out.println("shutdown");
            current.adapter.getCommunicator().shutdown();
        }
    }

    public static void main(String[] args) {
        int port = 11000;
        if (args.length > 0 && args[0].matches("\\d+")) {
            port = Integer.parseInt(args[0]);
        }

        try (Communicator communicator = Util.initialize(args)) {
            ObjectAdapter adapter = communicator.createObjectAdapterWithEndpoints(
                    "SimpleAdapter", "default -p " + port);
            adapter.add(new PrinterI(), Util.stringToIdentity("SimplePrinter"));
            adapter.activate();
            System.out.println("Servidor iniciado na porta " + port);
            System.out.flush();
            communicator.waitForShutdown();
        }
    }
}
