# Conversor HTML para PDF e Envio por E-mail

Este é um aplicativo simples que converte HTML para PDF usando a biblioteca WeasyPrint e envia o PDF gerado por e-mail. O aplicativo é construído usando Flask e é destinado a ser executado em um contêiner Docker.

## Configuração

Antes de executar o aplicativo, certifique-se de configurar as variáveis de ambiente no arquivo `.env`. As seguintes variáveis de ambiente são necessárias:

- `AWS_ACCESS_KEY_ID`: A chave de acesso da sua conta AWS para acesso ao serviço S3.
- `AWS_SECRET_ACCESS_KEY`: A chave secreta da sua conta AWS para acesso ao serviço S3.
- `AWS_S3_BUCKET_NAME`: O nome do bucket S3 onde os arquivos PDF serão armazenados.
- `AWS_S3_REGION`: A região do AWS S3 onde o bucket está localizado.
- `MAIL_FROM_ADDRESS`: O endereço de e-mail remetente para enviar o e-mail com o PDF.
- `MAIL_FROM_NAME`: O nome do remetente para exibição no e-mail.

## Como Executar

Certifique-se de ter o Docker e o Docker Compose instalados na sua máquina.

1. Clone o repositório para o seu ambiente local.
2. Navegue até o diretório raiz do projeto.
3. Crie um arquivo `.env` dentro da pasta app com as variáveis de ambiente conforme mencionado acima.
4. Execute o seguinte comando para construir e iniciar os contêineres Docker:

```bash
docker-compose up -d
```
Isso iniciará o aplicativo Flask e o servidor web estará acessível em `http://localhost:5000`.

## API Endpoints

### `POST /convert`

Este endpoint aceita uma solicitação JSON contendo o HTML a ser convertido para PDF e o endereço de e-mail para enviar o PDF.

Exemplo de corpo da solicitação:

```json
{
    "html": "<html><body><h1>Hello, World!</h1></body></html>",
    "email": "exemplo@email.com"
}
```

A resposta conterá a URL assinada do PDF gerado.

Exemplo de resposta:

```json
{
    "pdf_url": "https://s3.amazonaws.com/bucket-name/pdf-file.pdf"
}
```

## Notas

- O aplicativo gera um nome exclusivo para cada PDF gerado, incluindo um carimbo de data/hora e um identificador aleatório.
- O PDF gerado é armazenado temporariamente no serviço S3 e enviado por e-mail para o destinatário especificado.
- Certifique-se de definir permissões adequadas para a conta IAM associada às credenciais da AWS para acessar o bucket S3 e enviar e-mails via SES.

Este `README.md` fornece uma visão geral do aplicativo, incluindo configuração, instruções de execução e detalhes sobre os endpoints da API. Certifique-se de preencher os detalhes do ambiente, como as variáveis de ambiente AWS e os endereços de e-mail remetente, antes de executar o aplicativo.
