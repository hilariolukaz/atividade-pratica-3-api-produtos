import os
import tempfile

arquivo = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
arquivo.close()
os.environ['DB_PATH'] = arquivo.name
os.environ['API_KEY'] = 'chave-de-teste'

from fastapi.testclient import TestClient
from main import app

headers = {'x-api-key': 'chave-de-teste'}


def test_inicio_e_documentacao():
    with TestClient(app) as client:
        assert client.get('/').status_code == 200
        assert client.get('/openapi.json').status_code == 200
        assert client.get('/docs').status_code == 200


def test_seguranca():
    with TestClient(app) as client:
        assert client.get('/produtos').status_code == 401
        assert client.get('/produtos', headers={'x-api-key': 'errada'}).status_code == 401
        assert client.get('/produtos', headers=headers).status_code == 200


def test_fluxo_completo():
    with TestClient(app) as client:
        payload = {'nome': 'Cimento', 'preco': 35.9, 'quantidade': 10}
        resposta = client.post('/produtos', json=payload, headers=headers)
        assert resposta.status_code == 201
        id_ = resposta.json()['id']
        assert client.get(f'/produtos/{id_}', headers=headers).json()['nome'] == 'Cimento'
        assert any(p['id'] == id_ for p in client.get('/produtos', headers=headers).json())
        novo = {'nome': 'Areia fina', 'preco': 135, 'quantidade': 4}
        assert client.put(f'/produtos/{id_}', json=novo, headers=headers).json()['nome'] == 'Areia fina'
        assert client.delete(f'/produtos/{id_}', headers=headers).status_code == 204
        assert client.get(f'/produtos/{id_}', headers=headers).status_code == 404


def test_validacao():
    with TestClient(app) as client:
        resposta = client.post('/produtos', json={'nome': 'A', 'preco': -2, 'quantidade': -1}, headers=headers)
        assert resposta.status_code == 422
