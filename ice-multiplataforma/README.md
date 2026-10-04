# Ice Multiplataforma (Python e Java)

Mesmo contrato Slice (`Printer.ice`, da tarefa do `ice-demo/`) implementado em Python e Java:

| Cenário | Cliente | Servidor |
|---|---|---|
| 1 | Java (`java/PrinterClient.java`) | Python (`python/server.py`) |
| 2 | Python (`python/client.py`) | Java (`java/PrinterServer.java`) |

## Executar

Precisa de Java (`javac`) e Python 3 com ZeroC Ice 3.7. O jar do Ice para Java está em `lib/`.

```bash
python3 executar_cenarios.py      # os dois cenários
python3 executar_cenarios.py 1    # só o cenário 1
python3 executar_cenarios.py 2    # só o cenário 2
```

Manualmente (cenário 1):

```bash
python3 python/server.py 11000
javac -cp lib/ice-3.7.6.jar -d java/build $(find java -name '*.java')
java -cp java/build:lib/ice-3.7.6.jar PrinterClient 127.0.0.1 11000
```

Cenário 2:

```bash
java -cp java/build:lib/ice-3.7.6.jar PrinterServer 11000
python3 python/client.py 127.0.0.1 11000
```

## Regerar os stubs

```bash
slice2java --output-dir java/generated Printer.ice
slice2py   --output-dir python          Printer.ice
```

A discussão sobre middleware x transporte está em `RELATO_SUBMISSAO.txt`.
