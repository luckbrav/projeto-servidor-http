# Projeto Servidor HTTP em Python

## Integrantes
Bruno Maurici Passarella (RA:11202230516)
Lucas Gois Carneiro Batista (RA:11202111177)

## Descrição do Projeto
Este projeto consiste na implementação de um servidor Web capaz de interpretar comandos HTTP de diferentes clientes. O servidor foi desenvolvido "from scratch" (do zero), utilizando a linguagem Python 3.x e a biblioteca nativa de `sockets`. 

O objetivo principal é entender o funcionamento interno da Web e do protocolo HTTP/1.1, sem o uso de bibliotecas de alto nível ou frameworks que automatizem o processo.

## Funcionalidades
* **Comunicação via Sockets:** Estabelece conexão direta na porta 80 usando a API de sockets do Python.
* **Método GET (Com MIME Types):** O servidor recebe requisições, identifica a extensão do arquivo para enviar o `Content-Type` correto e envia o objeto de volta ao cliente (suportando arquivos HTML e imagens JPG/PNG em formato binário).
* **Método POST (Com suporte a segmentos TCP):** O servidor lê o cabeçalho `Content-Length` para garantir o recebimento seguro de dados pequenos ou grandes. O histórico de submissões é salvo no arquivo `BD.txt`.
* **Tratamento de Erros:** Caso o cliente solicite um recurso que não existe, o servidor responde adequadamente com um erro `404 Not Found`.

## Estrutura de Arquivos
De acordo com os requisitos, todos os objetos ficam no diretório raiz:
* `servidorHTTP.py`: Código principal do servidor.
* `index.html`: Página inicial solicitada pelo navegador.
* `ipsum.html`: Página contendo texto informativo e formatação CSS.
* `galeria.html`: Página secundária que exibe uma imagem carregada pelo servidor.
* `imagem.jpg`: Arquivo de imagem utilizado pela galeria.
* `BD.txt`: Arquivo gerado dinamicamente para armazenar os dados enviados via formulário POST.

## Como Executar
1. Certifique-se de ter o **Python 3.x** instalado.
2. Abra o terminal e navegue até a pasta raiz do projeto.
3. Execute o script do servidor:
   ```bash
   python servidorHTTP.py