import socket
import xml.etree.ElementTree as ET

# Função para extrair os parâmetros da chamada XML-RPC
def extract_params(xml_string):
    root = ET.fromstring(xml_string)
    params = root.findall(".//param/value/int")
    return [int(param.text) for param in params]

# Função que implementa o método "add_numbers" com dois parâmetros
def add_numbers(a, b):
    return a + b

HOST = 'localhost'
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

print('Aguardando conexão com o cliente')

conn, ender = s.accept()

print('Conectado em ', ender)

while True:
    data = conn.recv(1024)
    if not data:
        print('Fechando conexão')
        conn.close()
        break

    request = data.decode('utf-8')

    # Verifica se a mensagem é uma chamada de função XML-RPC
    if "<methodName>add_numbers</methodName>" in request:
        params = extract_params(request)
        if len(params) == 2:
            result = add_numbers(params[0], params[1])
        else:
            result = "Número incorreto de parâmetros"
        
        # Constrói a resposta XML-RPC
        response = f"""<?xml version='1.0'?>
            <methodResponse>
                <params>
                    <param>
                        <value><int>{result}</int></value>
                    </param>
                </params>
            </methodResponse>
        """
        
        # Envia a resposta de volta ao cliente
        conn.sendall(response.encode('utf-8'))
