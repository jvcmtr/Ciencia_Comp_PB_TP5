import socket
from q3_constants import *
import ssl

# CODIGO ADAPTADO A PARTIR DA QUESTÃO 4 DO TP4 DA DISCIPLINA DE PROJETO DE BLOCO

def send_messages(host, port, messages, decode_format=DEFAULT_DECODE_FORMAT, buffer_size=DEFAULT_BUFFER_SIZE, verbose=False):
    def prt(s, **kwargs):
        if verbose: print(s, **kwargs)
    addr = (host, port)

    prt("_____________________________________")
    prt("    EXECUTANDO CLIENT TLS")
    prt("[TCP CLIENT] Criando socket...", end="")

    context = ssl.create_default_context()
    # Nescessario pois o certificado é autoassinado
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tls_socket = context.wrap_socket(s)

    prt("Sucesso")

    prt(f"[TLS CLIENT] Estabelecendo conexão com {host}:{port} ... ", end="")
    tls_socket.connect(addr)
    prt("Sucesso")
    prt("--------------------------------------------------------")

    responses = []

    try:
        for m in messages:
            try:
                prt(f" Enviando mensagem para o servidor em {host}:{port} ... ", end="")
                tls_socket.sendall(m.encode(decode_format))
                prt(f"Mensagem enviada")

            except Exception as e:
                prt("!! FALHA !!")
                prt(e)
                responses.append(f"{e}")
            finally:
                prt("--------------------------------------------------------")
    finally:
        prt("[TLS CLIENT] Fechando, socket ... ", end="")
        tls_socket.close()
        prt("Sucesso")
        return messages

if __name__ == "__main__":
    send_messages(IP, PORT, ["Olá", "conxão segura"], verbose=True)




    