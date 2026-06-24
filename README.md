# Ciencia_Comp_PB_TP5
---

### Executando a questão 3 
Para realizar a questão 3 é nescessaria a instalação de bibliotecas e a geração de um certificado TLS.

Siga os seguintes passos:
1. Crie um certificado TLS:
```
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes
```
2. Crie e acesse um ambiente virtual:
```
python3 -m venv .venv
source .venv/bin/activate
```
3. Instale as dependencias do projeto:
```
pip install -r requirements.txt
```

**Especificamente para rodar o sniffer é nescessaria a permição de sudo**
Para executar um script python com essa permição dentro do ambiente virtual, 
execute o seguinte comando:
```
sudo ./.venv/bin/python3 q3_sniffer.py    
```

