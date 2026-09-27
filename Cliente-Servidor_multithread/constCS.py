# constCS.py
# Constantes de rede compartilhadas entre Cliente e Servidor

HOST = '127.0.0.1'       # Endereço IP padrão do servidor (localhost)
PORT = 5678              # Porta padrão do servidor principal
PORT_ALT = 5679          # Porta do servidor secundário (para testes com múltiplos servidores)
BACKLOG = 500            # Tamanho da fila de conexões pendentes do TCP
BUFFER_SIZE = 1024       # Tamanho do buffer de recepção do socket em bytes
TIMEOUT = 10.0           # Timeout em segundos para operações de socket
