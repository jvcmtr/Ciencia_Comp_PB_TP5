
import pcapy
import socket
from q3_constants import *


def sniff_package(header, data):
    try:        
        print(f"[+] Pacote TCP Capturado! Tamanho: {len(data)} bytes.")
        raw = [chr(b) for b in data]
        print(f"[Dados Brutos do Payload]: {data[:40]}")
        txt = "".join([chr(b) if 32 <= b <= 126 else "." for b in data])
        print(f"[Texto Convertido]: {txt[:40]}")
        if 'AUTH_TOKEN' not in txt:
            print(f"[-] Alerta: Padrão 'AUTH_TOKEN' NÃO encontrado. Os dados estão devidamente cifrados via TLS.")
        print()

    except Exception as e:
        print(f"[ERRO] {e}")
        raise e


if __name__ == "__main__":
    print("_____________________________________")
    sniffer = pcapy.open_live(INTERFACE, PACKET_LEN, False, TIMEOUT_MS)
    sniffer.setfilter(f"tcp port {PORT}")

    print(f"[*] Iniciando captura na interface {INTERFACE} (Porta: {PORT})....")
    try:
        sniffer.loop(0, sniff_package)
    except KeyboardInterrupt:
        print("[-] Encerrando programa")
    
    
    