# Implementação de um servidor HTTP/1.1 para interpretação de métodos GET e POST

import socket

# Endereço IP vazio aceita conexões de qualquer host local
SERVER_HOST = ""
# A porta deve ser a 80 para acessar diretamente http://localhost:80
SERVER_PORT = 80

# Criação e configuração do socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)

print(f"Servidor em execução...")
print(f"Escutando por conexões na porta {SERVER_PORT}")

# Loop para listening de conexões
while True:
    client_connection, client_address = server_socket.accept()

    # Lendo o primeiro bloco de dados da requisição
    request_bytes = client_connection.recv(4096)
    
    if request_bytes:
        # Separar o cabeçalho HTTP do Corpo da requisição
        partes = request_bytes.split(b"\r\n\r\n", 1)
        headers_raw = partes[0].decode(errors='ignore')
        body_bytes = partes[1] if len(partes) > 1 else b""
        
        # Analisar a primeira linha da requisição
        linhas_header = headers_raw.split("\n")
        primeira_linha = linhas_header[0].split()
        
        if len(primeira_linha) >= 2:
            metodo = primeira_linha[0] # "GET" ou "POST"
            filename = primeira_linha[1] # Caminho solicitado
            
            print(f"Recebido -> Método: {metodo} | arquivo: {filename}")

            # Se pediu a raiz, direcionando para o index
            if filename == "/":
                filename = "/index.html"
            
            # Removendo barra inicial para ler no diretório atual
            filepath = filename[1:]

            # ==========================================
            # LÓGICA DO MÉTODO GET
            # ==========================================
            if metodo == "GET":
                # Definindo o Content-Type dinâmico com base na extensão do arquivo
                if filepath.endswith(".html"):
                    content_type = "text/html; charset=utf-8"
                elif filepath.endswith(".jpg") or filepath.endswith(".jpeg"):
                    content_type = "image/jpeg"
                elif filepath.endswith(".png"):
                    content_type = "image/png"
                else:
                    content_type = "application/octet-stream"

                try:
                    # Lendo o arquivo em modo binário
                    with open(filepath, "rb") as fin:
                        content = fin.read()
                    
                    # Resposta de Sucesso dinâmica
                    response_header = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n"
                    client_connection.sendall(response_header.encode() + content)
                    
                except FileNotFoundError:
                    # Erro 404 formatado
                    response_header = "HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html; charset=utf-8\r\n\r\n"
                    html_erro = "<h1>ERRO 404!</h1><p>O arquivo solicitado nao foi encontrado no servidor!</p>"
                    client_connection.sendall(response_header.encode() + html_erro.encode())
            
            # ==========================================
            # LÓGICA DO MÉTODO POST
            # ==========================================
            elif metodo == "POST":
                # Procurar o cabeçalho Content-Length para saber o tamanho total dos dados
                content_length = 0
                for linha in linhas_header:
                    if linha.lower().startswith("content-length:"):
                        content_length = int(linha.split(":")[1].strip())
                
                # Continuar recebendo segmentos TCP até ler o arquivo inteiro (se for grande)
                while len(body_bytes) < content_length:
                    chunk = client_connection.recv(4096)
                    if not chunk:
                        break
                    body_bytes += chunk

                nome_novo_arquivo = "BD.txt"
                
                # Salvando os dados no servidor
                with open(nome_novo_arquivo, "ab") as fout:
                    fout.write(b"\n--- Nova Submissao POST ---\n")
                    fout.write(body_bytes)
                    fout.write(b"\n")
                
                # Tela simples de sucesso ao realizar POST formatada
                html_sucesso = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Sucesso!</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background-color: #f4f7f6; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background-color: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); text-align: center; }
        h1 { color: #2ecc71; margin-bottom: 10px; }
        p { color: #555; margin-bottom: 30px; font-size: 1.1em;}
        .btn { background-color: #3498db; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; transition: background 0.3s; }
        .btn:hover { background-color: #2980b9; }
    </style>
</head>
<body>
    <div class="card">
        <h1>Sucesso!</h1>
        <p>Recurso criado no servidor via método POST com êxito.</p>
        <a href="index.html" class="btn">Voltar para o início</a>
    </div>
</body>
</html>"""
                response = f"HTTP/1.1 201 Created\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{html_sucesso}"
                client_connection.sendall(response.encode())

    # Fechar a conexão
    client_connection.close()