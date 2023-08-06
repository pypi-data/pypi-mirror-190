
# DEBUG DE VARIAVEIS

Projeto criado com o intuito de facilitar o dabug de variavel em python

## Uso/Exemplos

```
Exemplo de uso

teste = [
          {
              "id": "637e0bbedaf70ce56a20e5aa",
              "email": "owen_colon@xylar.allfinanz",
              "roles": [
              "guest",
              "owner"
              ],
              "apiKey": "860a1784-ed4c-4e3f-962a-d3136e0b542a",
              "profile": {
              "dob": "1992-04-13",
              "name": "Owen Colon",
              "about": "Sint minim nisi dolor adipisicing sit. Duis id cillum nulla aliquip.",
              "address": "25 Homecrest Avenue, Elwood, Ohio",
              "company": "Xylar",
              "location": {
                  "lat": 29.216208,
                  "long": -39.477052
              }
              },
              "username": "owen92",
              "createdAt": "2010-12-17T23:32:45.095Z",
              "updatedAt": "2010-12-18T23:32:45.095Z"
                   }
        ]

debug("teste", exitDebug=True) -> função para ser utilizada

retorno da função abaixo

+------------+----------------+--------------------------------------------------------------+
| Variável   | Type           | Valor                                                        |
+============+================+==============================================================+
| teste      | <class 'list'> | [{'id': '637e0bbedaf70ce56a20e5aa', 'email':                 |
|            |                | 'owen_colon@xylar.allfinanz', 'roles': ['guest', 'owner'],   |
|            |                | 'apiKey': '860a1784-ed4c-4e3f-962a-d3136e0b542a', 'profile': |
|            |                | {'dob': '1992-04-13', 'name': 'Owen Colon', 'about': 'Sint   |
|            |                | minim nisi dolor adipisicing sit. Duis id cillum nulla       |
|            |                | aliquip.', 'address': '25 Homecrest Avenue, Elwood, Ohio',   |
|            |                | 'company': 'Xylar', 'location': {'lat': 29.216208, 'long':   |
|            |                | -39.477052}}, 'username': 'owen92', 'createdAt':             |
|            |                | '2010-12-17T23:32:45.095Z', 'updatedAt':                     |
|            |                | '2010-12-18T23:32:45.095Z'}]                                 |
+------------+----------------+--------------------------------------------------------------+
```
