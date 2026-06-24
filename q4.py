from scapy.all import ARP, Ether, srp, sniff

SUBNET = "192.168.0.12/24"
ETH_BROADCAST = "ff:ff:ff:ff:ff:ff"

def network_scanner(subnet):
    arp = ARP(pdst=subnet)
    ether = Ether(dst=ETH_BROADCAST)
    packet = ether / arp
    
    result = srp(packet, timeout=3, verbose=0)[0]
    data = {}
    
    for _, response in result:
        data[response.psrc] = response.hwsrc
        
    return data

def packet_sniffer(pkt, truth_table):
    if not pkt.haslayer(ARP): return
    if not pkt[ARP].op == 2: return

    ip_orig = pkt[ARP].psrc
    mac_orig = pkt[ARP].hwsrc

    valid = truth_table.get(ip_orig)

    print("+ Analizando pacote:")
    print(f"   - IP    : {ip_orig}")
    print(f"   - MAC   : {mac_orig}")
    print("+ Endereço MAC esperado para o IP:")
    print(f"   - MAC   : {valid}")
    print(f"   - VALIDO: {valid==mac_orig}")

    if not valid==mac_orig:
        print(f"[ALERTA] Possivel 'Man in The Midle Attack'. Endereço MAC esperado para o ip {ip_orig} é diferente da tabela de verdade.")


# Filtra apenas pacotes ARP

if __name__ == "__main__":
    print("_____________________________________")
    print(f"    Iniciando Network Scanner")
    print(f"+ Sub-rede: {SUBNET}")
    dt = network_scanner(SUBNET)
    
    print("\t IP \t | \t MAC")
    for ip, mac in dt.items():
        print(f"\t {ip} \t | \t {mac}")

    print("_____________________________________")
    print("    Iniciando Packet Sniffer")
    sniff(filter="arp", prn=lambda p: packet_sniffer(p, dt), store=0)