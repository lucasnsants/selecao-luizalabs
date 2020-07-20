## Processo Seletivo Luizalabs

### Instruções do uso do repositório

**Criando virtualenv**

```
python3 -m venv .venv
```


**Inicializando e desligando o virtualenv**

```
source .venv/bin/activate

deactive
```

**Instalando as dependências**

```
pip install -r requirements.txt
```

Caso não possua um banco de dados Postgres, disponibilizei um `docker-compose.yml` que contém dois bancos de dados, 1 para testes da API via *client*, outro para *testes automatizados*. Basta rodar os seguintes comandos

```
docker-compose up ou docker-compose up --build
```

- Os arquivos contendo as variáveis de ambientes para os dois ambientes:

- `.env` ~> desenvolvimento
- `.env.test` ~> testes

Para inicializar o servidor em *modo* de desenvolvimento: 

- `ENV_FILE_LOCATION=.env python run.py`

Para excutar todos os testes:

- `ENV_FILE_LOCATION=.env.test python -m unittest --buffer`

Executando único teste:

- `ENV_FILE_LOCATION=.env.test python -m unittest tests/test_user.py`

**Obs**: É necessário que todos os comandos sejam executados setando a variável `ENV_FILE_LOCATION` para que os bancos de dados não misturem-se.