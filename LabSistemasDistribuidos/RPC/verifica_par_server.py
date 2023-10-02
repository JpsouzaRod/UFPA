import socket
import xml.etree.ElementTree as ET

# Função para extrair o valor numérico de um elemento XML-RPC
def extract_value(xml_string):
    root = ET.fromstring(xml_string)
    value_element = root.find(".//value/int")
    if value_element is not None:
        return int(value_element.text)
    return None

# Função que implementa o método "is_even"
def is_even(n):
    return n % 2 == 0

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
    if "<methodName>is_even</methodName>" in request:
        param = extract_value(request)
        if param is not None:
            result = is_even(param)
        else:
            result = "Parâmetro inválido"
        
        # Constrói a resposta XML-RPC
        response = f"""
            <?xml version='1.0'?>
            <methodResponse>
                <params>
                    <param>
                        <value><boolean>{str(result).lower()}</boolean></value>
                    </param>
                </params>
            </methodResponse>
        """
        
        # Envia a resposta de volta ao cliente
        conn.sendall(response.encode('utf-8'))
