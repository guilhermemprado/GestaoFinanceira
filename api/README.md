# Minha API em REST

Este pequeno projeto faz parte do material diático da Disciplina **Desenvolvimento Full Stack Avançado** 

O objetivo aqui é apresetar uma API emplementada seguindo o estilo REST.

As principais tecnologias que serão utilizadas aqui é o:
 - [Flask](https://flask.palletsprojects.com/en/2.3.x/)
 - [SQLAlchemy](https://www.sqlalchemy.org/)
 - [OpenAPI3](https://swagger.io/specification/)
 - [Postgres](https://www.postgresql.org/)

---
### Instalação


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

---
### Executando o servidor


Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

---
### Acesso no browser

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

---
## Instalar e executar o Docker

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.


### Alguns comandos úteis do Docker

**Passo 2: Baixe a imagem do Postgres**
O próximo passo é baixar a imagem do Postgres a partir do Docker Hub. Para fazer isso, execute o seguinte comando em seu terminal:

    docker pull postgres


**Passo 3: Crie um volume para persistência de dados**
Antes de executar o contêiner, é importante criar um volume para persistência de dados. Isso garantirá que os dados do Postgres não sejam perdidos quando o contêiner for interrompido ou excluído. Para criar um volume, execute o seguinte comando em seu terminal:

    docker volume create pgdata


**Passo 4: Execute o contêiner Postgres**
Com o volume criado, agora você pode executar o contêiner Postgres. Para fazer isso, execute o seguinte comando em seu terminal:

    docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=sua-senha -v pgdata:/var/lib/postgresql/data postgres


Vamos explicar esse comando em mais detalhes:

    docker run: esse comando é utilizado para criar e executar um contêiner a partir de uma imagem.

    -d: essa opção indica que o contêiner será executado em segundo plano (modo detached).

    --name postgres: com essa opção, você pode dar um nome ao seu contêiner. Neste caso, estamos nomeando o contêiner como "postgres".

    -p 5432:5432: essa opção indica que estamos mapeando a porta 5432 do contêiner para a porta 5432 do host. A porta 5432 é a porta padrão do Postgres.

    -e POSTGRES_PASSWORD=sua-senha: essa opção define a variável de ambiente POSTGRES_PASSWORD com a senha que você escolher.

    -v pgdata:/var/lib/postgresql/data: essa opção define o volume pgdata criado anteriormente como o local onde os dados do Postgres serão armazenados.
    

postgres: esse é o nome da imagem que estamos utilizando para criar o contêiner.


**Passo 5: Acesse o banco de dados**
Agora que o contêiner do PostgreSQL está em execução, podemos nos conectar a ele usando qualquer cliente PostgreSQL. Vamos usar o psql, que é um cliente PostgreSQL de linha de comando.

Para conectar-se ao banco de dados, execute o seguinte comando no terminal:

    psql -h localhost -p 5432 -U postgres


**Passo 6: Gerencie o contêiner Postgres**
Você pode gerenciar o contêiner Postgres utilizando comandos Docker. Aqui estão alguns dos comandos mais úteis:

    docker start postgres: esse comando é utilizado para iniciar o contêiner Postgres se ele estiver parado.

    docker stop postgres: esse comando para o contêiner quando ele estiver em execução.

    docker rm postgres: quando o contêiner estiver parado, esse comando remove o contêiner.


>Para mais comandos, veja: (https://www.gasparbarancelli.com/post/passo-a-passo-como-criar-e-executar-um-container-postgres-com-docker).

>Diagrama base de dados: (https://github.com/guilhermemprado/GestaoFinanceira/blob/master/api/docs/Diagrama%20base%20de%20dados.jpg).