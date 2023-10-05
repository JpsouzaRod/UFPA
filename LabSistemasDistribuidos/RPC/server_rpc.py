import socket
import xml.etree.ElementTree as ET

def extract_params(root):
    params = root.findall(".//param/value/int")
    return [int(param.text) for param in params]

def execute_method(method_name, params):
    response_value = None
    if method_name == "add_numbers" and len(params) == 2:
        response_value = params[0] + params[1]
    elif method_name == "is_even" and params:
        response_value = 0 if params[0] % 2 == 0 else 1
    
    return response_value

def build_xml_rpc_response(method_name, response_value):
    return f"""<?xml version='1.0'?>
        <methodResponse>
            <methodName>{method_name}</methodName>
            <params>
                <param>
                    <value><int>{response_value}</int></value>
                </param>
            </params>
        </methodResponse>
    """

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
    root = ET.fromstring(request)
    
    method_name = root.find(".//methodName").text
    params = extract_params(root)

    result = execute_method(method_name, params)

    if result is not None:
        response = build_xml_rpc_response(method_name, result)
        conn.sendall(response.encode('utf-8'))