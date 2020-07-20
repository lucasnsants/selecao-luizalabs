## Processo Seletivo Luizalabs

### Instruções de uso do repositório

- Link para documentação da API: https://cutt.ly/FaY4DWq

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

Caso não possua um banco de dados Postgres instalado local, disponibilizei um `docker-compose.yml` que contém dois bancos de dados, 1 para testes da API via *client*, outro para *testes automatizados*. Basta rodar os seguintes comandos

```
docker-compose up ou docker-compose up --build
```

- Os arquivos contendo as variáveis de ambientes para os dois ambientes:

- `.env` ~> desenvolvimento
- `.env.test` ~> testes

Populando banco de dados

```
ENV_FILE_LOCATION=.env python seeds.py
```

Para inicializar o servidor em *modo* de desenvolvimento: 

- `ENV_FILE_LOCATION=.env python run.py`

Para excutar todos os testes:

- `ENV_FILE_LOCATION=.env.test python -m unittest --buffer`

Executando único teste:

- `ENV_FILE_LOCATION=.env.test python -m unittest tests/test_user.py`

**Obs**: É necessário que todos os comandos sejam executados setando a variável `ENV_FILE_LOCATION` para que os bancos de dados não misturem-se.

#### Tipos de usuários

Existe um sistema de *rule* que permite a criação de usuário com permissões de *admin*, assim o mesmo pode modificar e excluir dados do sistema.

- Lista de permissões do usuário admin:
    - cadastrar, atualizar e excluir produtos
    - cadastrar, excluir usuários

Basta fazer login com usuário com *rule* de **admin** e terá acesso a todos os endpoints do sistema.