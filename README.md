# Flask To-Do

Esta é uma aplicação de lista de tarefas (To-Do) construída com Flask. A API permite criar, ler, atualizar e excluir tarefas. A aplicação também inclui testes para garantir consistência dos endpoints.

## Instalação

### Pré-requisitos

- Python 3.8+
- Virtualenv

### Passos para Instalação

1. Clone o repositório:

```sh
git clone https://github.com/vpdiogo/flask-todo.git
cd flask-todo
```
2. Crie e ative um ambiente virtual:

```sh
python -m venv .env
source .env/bin/activate  # No Windows, use .env\Scripts\activate
```

3. Instale as dependências:

```sh
pip install -r requirements.txt
```

Execute para testar e verificar se o server roda sem erros:

```sh
python3 run.py
```

4. Configure o banco de dados:

Crie um diretório instance/ na raiz do repositório.
O arquivo settings.json deve ser adicionado no diretório instance/ e deve conter as seguintes configurações:

```json
{
    "DEBUG": true,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///todo.db",
    "SECRET_KEY": "your_secret_key",
    "SQLALCHEMY_TRACK_MODIFICATIONS": false
}
```

```sh
flask db stamp head
flask db upgrade
```

### Executar Testes

```sh
pytest
```

5. Execute a aplicação:

```sh
python run.py
```

A aplicação estará disponível em http://127.0.0.1:5000.

Se houver alguma inconsistência no banco de dados identificada ao interagir com a API, basta apagar o banco gerado no diretório instance/ e também remover o diretório migrations/, e então, executar os comandos abaixos para inicializar uma nova migration.

```sh
flask db init
flask db migrate -m "New migration"
flask db upgrade
```

### Estrutura do Projeto

```
flask-todo/
│
├── app/
│   ├── __init__.py
│   ├── api/
│   │   └── task_api.py
│   ├── models/
│   │   └── task.py
│   ├── services/
│   │   └── task_service.py
│   ├── utils/
│   │   └── response.py
│   │   └── logger.py
│   └── config.py
│
├── instance/
│   └── settings.json
│
├── migrations/
│   └── ... (arquivos de migração)
│
├── tests/
│   ├── conftest.py
│   └── test_task_api.py
│
├── run.py
├── pytest.ini
└── requirements.txt
```

#### Testes para as Rotas da API

- `GET /api/tasks/`: Retorna todas as tarefas podendo especificar filtro de "done"
- `GET /api/tasks/<int:id>`: Retorna uma tarefa específica pelo ID
- `POST /api/tasks/`: Cria uma nova tarefa
- `PATCH /api/tasks/<int:id>`: Atualiza uma tarefa existente pelo ID
- `DELETE /api/tasks/<int:id>`: Exclui uma tarefa pelo ID

## Rotas da API

### `GET /api/tasks/`

Retorna todas as tarefas.

Parâmetros de Consulta:

- page (int): O número da página. Padrão é 1.
- per_page (int): O número de itens por página. Padrão é 10.
- done (str): Filtro para tarefas concluídas (true) ou pendentes (false).

**Exemplo de Resposta:**

```json
{
    "tasks": [
        {
            "id": 1,
            "title": "Task 1",
            "description": "Description 1",
            "done": true,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        },
        {
            "id": 2,
            "title": "Task 2",
            "description": "Description 2",
            "done": false,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        }
    ],
    "total": 2,
    "page": 1,
    "per_page": 10,
    "items": 2
}
```

### `GET /api/tasks/<int:id>`

Retorna uma tarefa específica pelo ID.

**Exemplo de Resposta:**

```json
{
    "id": 1,
    "title": "Task 1",
    "description": "Description 1",
    "done": true,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
}
```

### `POST /api/tasks/`

Cria uma nova tarefa.

**Exemplo de Requisição:**

```json
{
    "title": "Task 3",
    "description": "Description 3",
    "done": false
}
```

**Exemplo de Resposta:**

```json
{
    "id": 3,
    "title": "Task 3",
    "description": "Description 3",
    "done": false,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
}
```

### `PATCH /api/tasks/<int:id>`

Atualiza uma tarefa existente pelo ID.

**Exemplo de Requisição:**

```json
{
    "title": "Updated Task 1",
    "description": "Updated Description 1",
    "done": true
}
```

**Exemplo de Resposta:**

```json
{
    "id": 1,
    "title": "Updated Task 1",
    "description": "Updated Description 1",
    "done": true,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": "2023-01-01T00:00:00"
}
```

### `DELETE /api/tasks/<int:id>`

Exclui uma tarefa pelo ID.

**Exemplo de Resposta:**

```json
{
    "message": "Task deleted successfully"
}
```
