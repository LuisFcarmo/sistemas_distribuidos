# ClientServerBasics (2.0) - Calculadora Remota Distribuída

**Disciplina:** Sistemas Distribuídos  
**Base Teórica:** Capítulo 02 (Arquiteturas de Sistemas Distribuídos - Comunicação Cliente-Servidor e Two-Party Communication / Fig. 2.3)

---

## 1. Descrição do Projeto

Este projeto consiste na evolução do exemplo básico de comunicação cliente-servidor via sockets TCP apresentado na aula (Capítulo 2, slide 5). 

O servidor original apenas ecoava o texto recebido adicionando um asterisco (`*`). Nesta implementação, o servidor foi transformado em um **Serviço de Calculadora Remota**, capaz de processar operações matemáticas enviadas pelo cliente através da rede, tratar exceções e retornar os resultados calculados de forma estruturada.

O cliente permite que o usuário faça **múltiplas requisições sequenciais** na mesma sessão, chamando funcionalidades diferentes a cada requisição por meio de um menu interativo ou executando uma demonstração automatizada de testes.

---

## 2. Arquitetura do Sistema

O sistema segue o modelo clássico **Cliente-Servidor centralizado (Two-party communication)** utilizando a API de sockets TCP (`SOCK_STREAM` sobre `AF_INET`):

```
+-------------------+                    +-------------------+
|      Cliente      |                    |     Servidor      |
|    (client.py)    |                    |    (server.py)    |
+-------------------+                    +-------------------+
          |                                        |
          |  1. TCP Handshake (connect)            | (listen / accept)
          |--------------------------------------->|
          |                                        |
          |  2. Envio de Requisição: "ADD 25 17"    |
          |--------------------------------------->| 3. Processamento
          |                                        |    (25 + 17 = 42)
          |  4. Resposta: "OK: 42"                 |
          |<---------------------------------------|
          |                                        |
          |  5. Próxima Requisição: "SQRT 144"     |
          |--------------------------------------->| 6. Processamento
          |                                        |    (sqrt(144) = 12)
          |  7. Resposta: "OK: 12"                 |
          |<---------------------------------------|
          |                                        |
          |  8. Encerramento: "QUIT"               |
          |--------------------------------------->| 9. Fecha conexão
          |                                        |
```

---

## 3. Especificação do Protocolo de Aplicação

A comunicação utiliza um protocolo textual simples baseado em linha de comando, no formato:
```
<OPERAÇÃO> [ARGUMENTO_1] [ARGUMENTO_2]
```

### 3.1. Operações Suportadas (Múltiplas Funcionalidades)

| Operação | Parâmetros | Descrição | Exemplo de Requisição | Exemplo de Resposta |
| :--- | :--- | :--- | :--- | :--- |
| **`ADD`** | `<a> <b>` | Soma dois números | `ADD 15 25` | `OK: 40` |
| **`SUB`** | `<a> <b>` | Subtrai `b` de `a` | `SUB 50 12` | `OK: 38` |
| **`MUL`** | `<a> <b>` | Multiplica `a` por `b` | `MUL 7 8` | `OK: 56` |
| **`DIV`** | `<a> <b>` | Divide `a` por `b` | `DIV 45 9` | `OK: 5` |
| **`POW`** | `<a> <b>` | Potenciação $a^b$ | `POW 2 10` | `OK: 1024` |
| **`SQRT`** | `<a>` | Raiz quadrada de `a` | `SQRT 81` | `OK: 9` |
| **`HELP`** | N/A | Exibe o manual de operações | `HELP` | *(Lista de comandos)* |
| **`QUIT`** | N/A | Encerra a conexão com o servidor | `QUIT` | `OK: Conexão encerrada pelo cliente.` |

### 3.2. Tratamento de Exceções e Erros

O servidor implementa validações defensivas para não quebrar perante requisições incorretas:
- **Divisão por zero:** `DIV 10 0` $\rightarrow$ `ERRO: Divisão por zero não é permitida.`
- **Raiz de número negativo:** `SQRT -16` $\rightarrow$ `ERRO: Não é possível calcular raiz quadrada de número negativo.`
- **Argumentos não numéricos:** `ADD abc 10` $\rightarrow$ `ERRO: Os parâmetros devem ser valores numéricos válidos.`
- **Número incorreto de parâmetros:** `ADD 10` $\rightarrow$ `ERRO: Operação ADD requer exatamente 2 parâmetros. Ex: ADD 10 5`
- **Operação não reconhecida:** `FATORIAL 5` $\rightarrow$ `ERRO: Operação desconhecida 'FATORIAL'. Digite HELP para ver os comandos disponíveis.`

---

## 4. Estrutura dos Arquivos

```
ClientServerBasics-2.0/
│
├── constCS.py     # Definição do HOST ('127.0.0.1') e PORT (5678)
├── server.py      # Servidor com parser, processamento matemático e socket TCP
├── client.py      # Cliente interativo com menu e modo de testes automatizados
└── README.md      # Documentação completa do sistema
```

---

## 5. Como Executar

### Pré-requisitos
- Python 3 instalado no sistema.

### Passo 1: Iniciar o Servidor
Abra um terminal, acesse a pasta do projeto e execute:
```bash
python3 server.py
```
O servidor ficará escutando na porta configurada aguardando clientes.

### Passo 2: Executar o Cliente
Em **outro terminal**, acesse a mesma pasta e execute:

#### Opção A: Cliente Interativo (Menu)
```bash
python3 client.py
```
Você poderá selecionar as operações pelo número do menu, digitar os valores e visualizar as respostas retornadas pelo servidor.

#### Opção B: Modo de Demonstração / Testes Automatizados
```bash
python3 client.py --demo
```
Executa automaticamente uma bateria de requisições cobrindo todas as operações (soma, subtração, multiplicação, divisão, potência, raiz quadrada, erros tratados, help e encerramento).

---

## 6. Publicação no GitHub

Para disponibilizar o projeto no seu repositório:

1. Crie um repositório no seu GitHub (por exemplo, `ClientServerBasics-2.0`).
2. No seu terminal, dentro da pasta do projeto, execute:
   ```bash
   git init
   git add constCS.py server.py client.py README.md
   git commit -m "Implementação da Calculadora Remota Cliente-Servidor (sockets TCP)"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/ClientServerBasics-2.0.git
   git push -u origin main
   ```
3. Copie o link do seu repositório e envie no campo da tarefa do curso.
# sistemas_distribuidos
