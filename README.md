# Pre-Requisites:
* **Iniciar o docker:** sudo docker-compose up
* **Correr as migrações (modelo de dados):** sudo docker-compose run app python manage.py migrate
* **Aplicar alterações na base de dados:** sudo docker-compose run app python manage.py makemigrations
* **Criar utilizador super (administrador de sistema):** sudo docker-compose run app python manage.py createsuperuser
* **Inserir dados na base de dados para tabelas de estados e categorias:** sudo docker-compose run app python manage.py loaddata data_to_db.json

# Run Docker:
**sudo docker-compose up**

# API:
## Occurrences
* Retorna a lista de ocorrências criadas, ordenadas por data de modificação. As ocorrências podem ser filtradas por autor, categoria ou localização (latitude + longitude + raio de alcance). Também permite a criação de uma nova ocorrência.
### Métodos suportados
Método | URL | Descrição
------------ | ------------- | -------------
GET | /occurences/ | Retorna uma lista com o detalhe de cada ocorrência.
POST | /occurences/ | Envia um objecto com o detalhe da ocorrência a criar.

### Pedido / Resposta
#### GET
Atributo | Tipo | Descrição
------------ | ------------- | -------------
id | Número | Identificador único da ocorrência.
description | Texto | Descrição da ocorrência.
geo_location | Coordenadas | Coordenadas (longitude / latitude) da ocorrência.
author | Texto | Autor da ocorrência.
creation_date | Data | Data de criação da ocorrência.
modified_date | Data | Data de alteração da ocorrência.
occurence_state_id | Número | Identificador único do estado da ocorrência.
occurence_state | Objeto | Detalhes do estado da ocorrência (id, descrição)
occurence_category_id | Número | Identificador único da categoria da ocorrência.
occurence_category | Objeto | Detalhes da categoria da ocorrência (id, label, descrição)

```json
GET /occurences/
-----------------------------------------------
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
[
    {
        "id": 1,
        "description": "test001",
        "geo_location": "SRID=4326;POINT (-8.601823849656101 39.14157515041888)",
        "author": "author001",
        "creation_date": "2019-03-31 00:11:51",
        "modified_date": "2019-03-31 00:26:43",
        "occurence_state_id": 3,
        "occurence_state": {
            "id": 3,
            "description": "resolvido"
        },
        "occurence_category_id": 1,
        "occurence_category": {
            "id": 1,
            "label": "CONSTRUCTION",
            "description": "planned road work"
        }
    }
]
```

#### POST
Atributo | Tipo | Descrição
------------ | ------------- | -------------
description | Texto | Descrição da ocorrência.
occurence_category_id | Número | Identificador único da categoria da ocorrência.

```json
POST /occurences/
{
    "description": "test001",
    "occurence_category_id": 1,
}
-----------------------------------------------
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
{
    "success": "Occurence test001 created successfully"
}
```

## Occurrences update
* Permite a alteração de uma ocorrência já existente. Apenas pode ser alterado o estado da mesma e por um administrador do sistema (superuser).

### Métodos suportados
Método | URL | Descrição
------------ | ------------- | -------------
PUT | /occurences/id/ | Envia um objecto com o estado da ocorrência a editar.

### Pedido / Resposta
#### PUT
Atributo | Tipo | Descrição
------------ | ------------- | -------------
occurence_state_id | Número | Identificador único do estado da ocorrência.

```json
POST /occurences/
{
    "occurence_state_id": 2,
}
-----------------------------------------------
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
{
    "success": "Occurence test001 updated successfully"
}
```

# ADMIN 
Esta aplicação também disponibiliza o portal para o administrador do sistema. Pode com isso criar, editar ou ver ocorrências.
