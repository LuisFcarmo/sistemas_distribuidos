# ZeroC Ice Demo - Invocação Remota de Objetos (RPC)

**Disciplina:** Sistemas Distribuídos — UFG  
**Base Teórica:** Capítulo 3 (Exemplo 3.21 de Maarten van Steen)  
**Repositório de Referência:** [https://github.com/professorfabio/ice-demo](https://github.com/professorfabio/ice-demo)  
**Documentação de Referência:** [ZeroC Ice Documentation](https://docs.zeroc.com/ice/3.8/cpp/get-started)

---

## 1. Descrição da Tarefa

Esta tarefa consiste na extensão do exemplo base de comunicação com **ZeroC Ice** (middleware orientado a objetos distribuídos), adicionando **novos métodos remotos** à interface Slice original e implementando-os no servidor e cliente.

---

## 2. Interface Slice (`Printer.ice`)

A interface original continha apenas o método `printString`. Foram acrescentados novos métodos com diferentes tipos de parâmetros e retornos (strings, inteiros e controle de ciclo de vida):

```slice
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
```

---

## 3. Estrutura dos Arquivos

```text
ice-demo/
├── Printer.ice       # Contrato Slice com método original + novos métodos
├── Printer_ice.py   # Código Python gerado pelo compilador slice2py
├── Demo/             # Pacote gerado contendo esqueletos e stubs do Ice
├── server.py         # Servidor que implementa o servant PrinterI com todos os métodos
├── client.py         # Cliente que invoca os métodos remotos via proxy tipado
├── server2.py        # Demonstração de múltiplos servants no mesmo adapter
├── client2.py        # Cliente para invocações nos múltiplos servants
├── executar_teste.py # Script de demonstração automatizada (inicia servidor e testa cliente)
└── README.md         # Documentação desta pasta
```

---

## 4. Guia de Execução

### Opção 1: Execução Automática em 1 Comando (Recomendado)

Na pasta `ice-demo/`:
```bash
python3 executar_teste.py
```
*Ou a partir da raiz do repositório:*
```bash
python3 executar_ice.py
```

### Opção 2: Execução Manual (2 Terminais)

#### Terminal 1: Iniciar o Servidor
```bash
python3 server.py
```
*(Opcionalmente, especifique uma porta: `python3 server.py 11000`)*

#### Terminal 2: Executar o Cliente
```bash
python3 client.py
```
*(Opcionalmente, passe host e porta: `python3 client.py 127.0.0.1 11000`)*

---

## 5. Como Recompilar o Contrato Slice

Caso modifique o arquivo `Printer.ice`, recompile com:
```bash
slice2py Printer.ice
```
*(Isso atualizará `Printer_ice.py` e o pacote `Demo/` automaticamente)*.
