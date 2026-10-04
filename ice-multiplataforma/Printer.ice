module Demo
{
    interface Printer
    {
        string printString(string s);
        string toUpper(string s);
        int add(int a, int b);
        string repeatString(string s, int times);
        void shutdown();
    }
}
