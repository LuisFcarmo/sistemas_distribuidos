// Printer.ice
// Definição da interface Slice para ZeroC Ice
// Disciplina: Sistemas Distribuídos - UFG
// Referência: https://github.com/professorfabio/ice-demo e Maarten van Steen (Exemplo 3.21)

module Demo
{
    interface Printer
    {
        // Método original do exemplo base:
        string printString(string s);

        // Novos métodos adicionados conforme requisito da tarefa:
        // 1. Converte string recebida para letras maiúsculas no servidor e retorna o resultado
        string toUpper(string s);

        // 2. Realiza a soma de dois inteiros remotamente e retorna o resultado
        int add(int a, int b);

        // 3. Repete a string s 'times' vezes no servidor e retorna o texto resultante
        string repeatString(string s, int times);

        // 4. Encerramento gracioso remoto do servidor
        void shutdown();
    }
}
