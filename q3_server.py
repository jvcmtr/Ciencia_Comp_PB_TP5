import socket
from q3_constants import *
import ssl

# CODIGO ADAPTADO A PARTIR DA QUESTÃO 4 DO TP4 DA DISCIPLINA DE PROJETO DE BLOCO

def _on_message_recieved(client, message):
    print(f" Mensagem recebida do cliente: {client}")
    print(f" Mensagem: \t({len(message)} caracteres)")
    print('"' + message + '"')
    return message

def start_tls_server(buffer_size=DEFAULT_BUFFER_SIZE, decode_format=DEFAULT_DECODE_FORMAT, verbose=False, handler=_on_message_recieved):
    def prt(s, **kwargs):
        if verbose: print(s, **kwargs)

    prt("_______________________________")
    prt("    INICIANDO SEVER TLS ")

    try:
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=CERTIFICATE, keyfile=KEY)
    except:
        print("ERRO: Os arquivos de chave e certificado não foram encontrados, crie estes arquivos utilizando o seguinte comando")
        print("openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDR)
    s.listen()
    prt(f"[TLS SEVER] Socket ativo em: {ADDR}")

    while True:
        try:
            conection, client = s.accept()
            tls_con = context.wrap_socket(conection, server_side=True)
            prt(f"[TLS SEVER] Conexão segura estabelecida com {client[0]}:{client[1]}")
            prt("--------------------------------------------------------")
            while True:
                data = tls_con.recv(buffer_size)
                if not data: break
                msg = data.decode(decode_format)
                handler(client, msg)
            prt("--------------------------------------------------------")
            prt(f"[TLS SEVER] Conexão encerrada com o cliente. {client[0]}:{client[1]}")
            tls_con.close()
        
        except Exception as e:
            raise e
            print(f"\t[ERRO] [TLS SEVER] Uma falha ocorreu ao processar uma mensagem: {e}")


    prt("[TLS SEVER] Fechando socket...", end="")
    s.close()
    prt("Sucesso")

if __name__ == "__main__":
    start_tls_server(verbose=True)



    