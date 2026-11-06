"""API simples de produtos para a disciplina Arquitetura de APIs."""
import os
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field

DB_PATH = os.getenv('DB_PATH', 'produtos.db')
API_KEY = os.getenv('API_KEY', 'chave-faculdade-2026')


def conectar():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def criar_banco():
    with conectar() as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT NOT NULL, preco REAL NOT NULL, quantidade INTEGER NOT NULL)')


@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_banco()
    yield


app = FastAPI(title='API de Controle de Produtos', version='1.0.0', description='Atividade Prática 3 - Arquitetura de APIs', lifespan=lifespan)


class ProdutoEntrada(BaseModel):
    nome: str = Field(min_length=2, max_length=100, examples=['Cimento'])
    preco: float = Field(gt=0, examples=[35.90])
    quantidade: int = Field(ge=0, examples=[10])


class Produto(ProdutoEntrada):
    id: int


def autenticar(x_api_key: Annotated[str | None, Header()] = None):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Chave de acesso inválida ou ausente')


@app.get('/', tags=['Informações'])
def inicio():
    return {'mensagem': 'API funcionando. Acesse /docs para testar.'}


@app.get('/produtos', response_model=list[Produto], tags=['Produtos'])
def listar(_: None = Depends(autenticar)):
    with conectar() as conn:
        return [dict(row) for row in conn.execute('SELECT * FROM produtos ORDER BY id')]


@app.get('/produtos/{produto_id}', response_model=Produto, tags=['Produtos'])
def buscar(produto_id: int, _: None = Depends(autenticar)):
    with conectar() as conn:
        row = conn.execute('SELECT * FROM produtos WHERE id = ?', (produto_id,)).fetchone()
    if row is None:
        raise HTTPException(404, 'Produto não encontrado')
    return dict(row)


@app.post('/produtos', response_model=Produto, status_code=201, tags=['Produtos'])
def cadastrar(produto: ProdutoEntrada, _: None = Depends(autenticar)):
    with conectar() as conn:
        cursor = conn.execute('INSERT INTO produtos (nome, preco, quantidade) VALUES (?, ?, ?)', (produto.nome, produto.preco, produto.quantidade))
        produto_id = cursor.lastrowid
    return {'id': produto_id, **produto.model_dump()}


@app.put('/produtos/{produto_id}', response_model=Produto, tags=['Produtos'])
def atualizar(produto_id: int, produto: ProdutoEntrada, _: None = Depends(autenticar)):
    with conectar() as conn:
        existe = conn.execute('SELECT id FROM produtos WHERE id = ?', (produto_id,)).fetchone()
        if existe is None:
            raise HTTPException(404, 'Produto não encontrado')
        conn.execute('UPDATE produtos SET nome = ?, preco = ?, quantidade = ? WHERE id = ?', (produto.nome, produto.preco, produto.quantidade, produto_id))
    return {'id': produto_id, **produto.model_dump()}


@app.delete('/produtos/{produto_id}', status_code=204, tags=['Produtos'])
def excluir(produto_id: int, _: None = Depends(autenticar)):
    with conectar() as conn:
        cursor = conn.execute('DELETE FROM produtos WHERE id = ?', (produto_id,))
        if cursor.rowcount == 0:
            raise HTTPException(404, 'Produto não encontrado')
