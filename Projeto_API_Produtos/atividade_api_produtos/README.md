# Sistema de Controle de Produtos

Projeto de API REST para a disciplina Arquitetura de APIs. Usei Python, FastAPI e SQLite para implementar um cadastro simples de produtos.

## Como executar

1. Instale Python 3.10 ou superior.
2. Abra o terminal na pasta do projeto.
3. Instale as dependências: `pip install -r requirements.txt`
4. Inicie o servidor: `python -m uvicorn main:app --reload`
5. Acesse `http://127.0.0.1:8000/docs` para visualizar o Swagger.

## Segurança

As rotas de produtos exigem o cabeçalho `x-api-key` com o valor `chave-faculdade-2026` (somente para demonstração local). No Swagger, clique em **Try it out**, informe o cabeçalho e execute. Em produção, a chave deve ser alterada por variável de ambiente `API_KEY` e nunca divulgada publicamente.

## Rotas

| Método | Caminho | Função |
|---|---|---|
| GET | `/` | Verificar API |
| GET | `/produtos` | Listar produtos |
| GET | `/produtos/{id}` | Consultar produto |
| POST | `/produtos` | Cadastrar produto |
| PUT | `/produtos/{id}` | Atualizar produto |
| DELETE | `/produtos/{id}` | Excluir produto |

Exemplo de cadastro: `{"nome":"Cimento","preco":35.90,"quantidade":10}`.

## Testes

Execute `python -m pytest -v`. Os testes verificam acesso, documentação, segurança, cadastro, listagem, atualização, exclusão e validação de dados.

## Observações

O banco `produtos.db` é criado automaticamente na primeira execução. Este é um projeto didático, não um sistema pronto para produção.
