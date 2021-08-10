# Kanvas

Uma API desenvolvida para ajudar no gerenciamento educacional de escolas de programação. Funciona como uma pequena plataforma na qual podem ser cadastrados instrutores e facilitadores de ensino, além de estudantes, cursos e atividades. Os alunos podem submeter as atividades realizadas, que serão corrigidas pelos facilitadores. É como se fosse um mini Canvas, daí o nome Kanvas.


## Instalação
#### No terminal, siga os seguintes passos:
Crie uma pasta na sua máquina e baixe o projeto:

    git clone https://gitlab.com/Haguken/kanvas.git
<br>
Entre na pasta, crie um ambiente virtual e entre nele:

    cd kenzie-pet && python3 -m venv venv && source venv/bin/activate
<br>
Instale as dependências:

    pip install -r requirements.txt
<br>
Crie as tabelas do banco de dados:

    python3 manage.py migrate
<br>
Rode o sistema em http://127.0.0.1:8000/ digitando:

    python3 manage.py runserver
<br>

## Utilização
É requerido um API client como, por exemplo, o [Postman](https://www.postman.com/downloads/)
### Rotas:
<br>


#### POST /api/accounts/
#### Criação de um usuário
A API funcionará com autenticação baseada em token. Além disso, as permissões de usuários são definidas pela seguinte tabela:

| Atributo | Instrutor | Facilitador | Estudante
| ------ | ------ | ------ | ------
| is_superuser | True | False | False 
| is_staff | True | True | False

```
// REQUEST
      {
        "username": "student",
        "password": "1234",
        "is_superuser": false,
        "is_staff": false
      }
```
```
// RESPONSE STATUS -> HTTP 201
      {
        "id": 1,
        "username": "student",
        "is_superuser": false,
        "is_staff": false
      }
```
<br>

    
####  POST /api/login/
#### Fazendo login(qualquer tipo de usuário):

```
// REQUEST
      {
        "username": "student",
        "password": "1234"
      }
```


```
// RESPONSE STATUS -> HTTP 200
      {
        "token": "dfd384673e9127213de6116ca33257ce4aa203cf"
      }
```



<br>

### Cursos
Course representa um curso dentro da plataforma Kanvas. Apenas um User com acesso de instrutor (ou seja is_superuser == True) pode criar novos cursos, matricular usuários nos cursos e excluir cursos.

#### POST /api/courses/
#### Criando um curso:

```
// REQUEST
      // Header -> Authorization: Token <token-do-instrutor>
      {
        "name": "Node"
      }
```

   
```
// RESPONSE STATUS -> HTTP 201
      {
        "id": 1,
        "name": "Node",
        "users": []
      }
```
<br>

 #### PUT /api/courses/<int:course_id>/registrations/
#### Atualizar lista de estudantes matriculados em um curso

```
// REQUEST
      // Header -> Authorization: Token <token-do-instrutor>
      {
        "user_ids": [3, 4, 5]
      }
```


```
// RESPONSE STATUS -> HTTP 200
      {
        "id": 1,
        "name": "Node",
        "users": [
          {
            "id": 3,
            "username": "student1"
          },
          {
            "id": 4,
            "username": "student2"
          },
          {
            "id": 5,
            "username": "student3"
          }
        ]
      }
```

<br>

#### GET /api/courses/
#### Obter lista de cursos e alunos matriculados(qualquer usuário pode acessar, inclusive que não está autenticado)

```
// RESPONSE STATUS -> HTTP 200
      [
        {
          "id": 1,
          "name": "Node",
          "users": [
            {
              "id": 3,
              "username": "student1"
            }
          ]
        },
        {
          "id": 2,
          "name": "Django",
          "users": []
        },
        {
          "id": 3,
          "name": "React",
          "users": []
        }
      ]
```
<br>

#### GET /api/courses/<int:course_id>/
#### Obter um curso específico(livre acesso também)

```
// RESPONSE STATUS -> HTTP 200
      {
        "id": 1,
        "name": "Node",
        "users": [
          {
            "id": 3,
            "username": "student1"
          }
        ]
      }
```
<br>

#### DELETE /api/courses/<int:course_id>/
#### Deletar um curso

```
// REQUEST
      // Header -> Authorization: Token <token-do-instrutor>
```


`// RESPONSE STATUS -> HTTP 204 NO CONTENT`

<br>

### Atividades e submissões:
Ativity representa uma atividade cadastrada no sistema pelos facilitadores ou instrutores para que os alunos possam fazer suas submissões.

Submission representa uma submissão de uma atividade feita por um aluno.


#### POST /api/activities/
#### Criando uma atividade

```
// REQUEST
// Header -> Authorization: Token <token-do-facilitador ou token-do-instrutor>
{
  "title": "Kenzie Pet",
  "points": 10
}
```

```
// RESPONSE STATUS -> HTTP 201
      {
        "id": 1,
        "title": "Kenzie Pet",
        "points": 10,
        "submissions": []
      }
```

<br>

#### GET /api/activities/
#### Listar atividades

```
// REQUEST
// Header -> Authorization: Token <token-do-instrutor ou token-do-facilitador>
```


```
// RESPONSE STATUS -> HTTP 200
[
        {
          "id": 1,
          "title": "Kenzie Pet",
          "points": 10,
          "submissions": [
            {
              "id": 1,
              "grade": 10,
              "repo": "http://gitlab.com/kenzie_pet",
              "user_id": 3,
              "activity_id": 1
            }
          ]
        },
        {
          "id": 2,
          "title": "Kanvas",
          "points": 10,
          "submissions": [
            {
              "id": 2,
              "grade": 8,
              "repo": "http://gitlab.com/kanvas",
              "user_id": 4,
              "activity_id": 2
            }
          ]
        },
        {
          "id": 3,
          "title": "KMDb",
          "points": 9,
          "submissions": [
            {
              "id": 3,
              "grade": 4,
              "repo": "http://gitlab.com/kmdb",
              "user_id": 5,
              "activity_id": 3
            }
          ]
        }
      ]
```

<br>

#### POST /api/activities/<int:activity_id>/submissions/
#### Submeter uma atividade

```
// REQUEST
      // Header -> Authorization: Token <token-do-estudante>
      {
        "grade": 10, // Esse campo é opcional(será sempre nulo quando o estudante faz uma submissão)
        "repo": "http://gitlab.com/kenzie_pet"
      }
```

    
```
// RESPONSE STATUS -> HTTP 201
      {
        "id": 7,
        "grade": null,
        "repo": "http://gitlab.com/kenzie_pet",
        "user_id": 3,
        "activity_id": 1
      }
```
<br>

#### PUT /api/submissions/<int:submission_id>/
#### Editar a nota de uma submissão

```
// REQUEST
// Header -> Authorization: Token <token-do-facilitador ou token-do-instrutor>
{
  "grade": 10
}
```


 ```
// RESPONSE STATUS -> HTTP 200
      {
        "id": 3,
        "grade": 10,
        "repo": "http://gitlab.com/kenzie_pet",
        "user_id": 3,
        "activity_id": 1
      }
```
<br>

#### GET /api/submissions/
#### Listar submissões(somente usuários autenticados)
- Para um estudante, serão listadas somente as submissões realizadas por ele.
```
//REQUEST
      //Header -> Authorization: Token <token-do-estudante>
```

```
// RESPONSE STATUS -> HTTP 200
      [
        {
          "id": 2,
          "grade": 8,
          "repo": "http://gitlab.com/kanvas",
          "user_id": 4,
          "activity_id": 2
        },
        {
          "id": 5,
          "grade": null,
          "repo": "http://gitlab.com/kmdb2",
          "user_id": 4,
          "activity_id": 1
        }
      ]
```
<br>

- Para um instrutor ou facilitador serão listadas as submissões de todos os alunos
```
//REQUEST
//Header -> Authorization: Token <token-do-facilitador ou token-do-instrutor>
```


```
// RESPONSE STATUS -> HTTP 200
      [
        {
          "id": 1,
          "grade": 10,
          "repo": "http://gitlab.com/kenzie_pet",
          "user_id": 3,
          "activity_id": 1
        },
        {
          "id": 2,
          "grade": 8,
          "repo": "http://gitlab.com/kanvas",
          "user_id": 4,
          "activity_id": 2
        },
        {
          "id": 3,
          "grade": 4,
          "repo": "http://gitlab.com/kmdb",
          "user_id": 5,
          "activity_id": 3
        },
        {
          "id": 4,
          "grade": null,
          "repo": "http://gitlab.com/kmdb2",
          "user_id": 5,
          "activity_id": 3
        }
      ]
```
<br>


## Tecnologias usadas
- Django
- Djando Rest Framework
- SQLite
## License
MIT


