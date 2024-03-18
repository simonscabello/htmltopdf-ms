# HTML to PDF Microservice

Este é um microserviço simples para converter HTML em PDF. Ele utiliza o Flask para criar uma API que recebe HTML em formato JSON e retorna o PDF correspondente.

## Instalação

Certifique-se de ter o Python e o pip instalados. Em seguida, você pode instalar as dependências do projeto executando o seguinte comando no diretório raiz do projeto:

```bash
pip install -r requirements.txt
```

## Configuração

O arquivo `.env` contém variáveis de ambiente que podem ser configuradas conforme necessário para o seu ambiente de desenvolvimento. Certifique-se de definir as variáveis de ambiente apropriadas antes de iniciar o servidor.

## Execução

Para executar o servidor Flask, basta executar o seguinte comando no diretório `app`:

```bash
python app.py
```


Isso iniciará o servidor Flask na porta padrão (5000).

## Uso da API

A API deste microserviço aceita solicitações POST contendo HTML no formato JSON e retorna o PDF correspondente.

Aqui está um exemplo de como você pode usar a API usando `curl`:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"html": "<html><body><h1>Hello, World!</h1></body></html>"}' \
  http://localhost:5000/convert \
  --output output.pdf
```