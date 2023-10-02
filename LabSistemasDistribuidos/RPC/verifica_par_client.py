import socket
import xml.etree.ElementTree as ET

# Função para construir uma chamada de método XML-RPC
def build_xml_rpc_request(method_name, params):
    request = f"""<?xml version='1.0'?>
        <methodCall>
            <methodName>{method_name}</methodName>
            <params>
    """

    for param in params:
        request += f"""
                <param>
                    <value><int>{param}</int></value>
                </param>
        """
    
    request += """
            </params>
        </methodCall>
    """
    
    return request

# Função para extrair o valor booleano de um elemento XML-RPC
def extract_value(xml_string):
    # Remover qualquer espaço em branco ou caracteres não XML no início da string
    xml_string = xml_string.strip()
    
    root = ET.fromstring(xml_string)
    value_element = root.find(".//value/boolean")
    if value_element is not None:
        return bool(value_element.text)
    return None

HOST = 'localhost'
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Chamada de função remota 1
method_name = "is_even"
params = [170]
request = build_xml_rpc_request(method_name, params)

s.sendall(request.encode('utf-8'))

response = s.recv(1024).decode('utf-8')

# Analisa a resposta XML-RPC

param = extract_value(response)
if param is not None:
    print("170 é par:", param)  # Use a variável 'param' em vez de 'response'
else:
    result = "Retorno inválido"
            
s.close()
