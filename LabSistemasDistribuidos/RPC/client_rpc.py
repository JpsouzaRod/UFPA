import socket
import xml.etree.ElementTree as ET

# Função para extrair o valor booleano da resposta XML-RPC
def extract_int_value(xml_string):
    root = ET.fromstring(xml_string)
    value_element = root.find(".//value/int")
    return int(value_element.text)

def xml_rpc_request(method_name, params):
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


HOST = 'localhost'
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Chamada de função remota com dois parâmetros

method_name = input("Digite o nome do metodo: ")

params = input("Digite uma lista de números: ")
params = [int(x) for x in params.split(",")]

request = xml_rpc_request(method_name, params)
s.sendall(request.encode('utf-8'))

response = s.recv(1024).decode('utf-8')

if "add_numbers" in response:
    result = extract_int_value(response)
    print(f"{params[0]} + {params[1]} = ", result)


if "is_even" in response:
    result = extract_int_value(response)
    if result == 0:
        print(f"{params[0]} é par")
    else:
        print(f"{params[0]} é impar")
 
    
s.close()
