
# Aprendiendo fastAPI

## Instalaciones necesarias

- Python (versión 3.6 en adelante por hint types y data validation)

- [fastAPI](https://fastapi.tiangolo.com/tutorial/) 
    
***pueden encontrar las librerías en el 'requirements.txt'***

## Entendiendo la app

fastAPI es un framework extremadamente rápido lo importante es entender la estructura básica de los endpoints

```python
from fastapi import FastAPI

# instancia de la clase FastAPI
app = FastAPI()


# nuestro primer endpoint en el root
@app.get("/")
def home():
    return {"message": "esto es lo que se va a mostrar"}
```
    

el orden importa. Si tuvieramos otros método que sea:

```python
@app.get("/")
def greetings():
    return {"message": "Hola ¿cómo estás terrícola?"}
```
renderizaría sólo la primer coincidencia, en este caso la función home.

## HTTP Requests Methods & Status codes

es importante entender como nos comunicamos con el servidor. Cada uno de los métodos http tiene una función específica que podemos entender mediante la documentación de mozilla:

- [Métodos HTTP](https://developer.mozilla.org/es/docs/Web/HTTP/Methods)
- [Códigos de estado](https://developer.mozilla.org/es/docs/Web/HTTP/Status)

> Recordar que el método POST puede enviar data al servidor, 
> por lo tanto tiene una diferencia, tiene cuerpo (body)

## Validando esquemas

como hemos visto, el método post, nos permite enviar data al servidor mediante un JSON, que asemeja a un diccionario de python.

¿Cómo podemos asegurarnos que nos envíen en cada endpoint del tipo POST, los datos que necesitamos?
La respuesta es con un esquema. Acá aparece pydantic.

```python
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    lastname: str
    email: str
    password: str
    DoB: Optional[date] = "1900-01-01"

@app.post("/login")
def login(user: User):

    # transforma el modelo a diccionario
    user.dict()

    data = {"santiago": {"name": "Santiago", "password": "admin1234"}}

    if user.name in data.keys():
        if user.password == data[user.name]["password"]:
            return "You are logged"
    return "Your credentials are incorrect"
    
```

de esta manera forzamos a que el usuario envíe lo que nosotros necesitamos como data y de no hacerlo de esta manera según los campos requeridos, lanzaremos un error.
Por otro lado hay que saber que cada modelo de pydantic puede transformarse a un diccionario de python, mediante el método "***.dict()***"

## Conectando la app a PostgreSQL

En mi caso puntual monté un postgres mediante docker, pero se puede seguir la instalación por defecto de postgres tanto para MacOS, windows o linux.

Para conectarnos a postgres desde python, necesitamos la librería psycopg. La misma la instalamos desde la terminal usando pip

```python
pip install psycopg2-binary
```

Una vez instalada, necesitamos importarla en nuestra app mediante el comando:
`import psycopg2`

Generamos la conexión y el cursor que es quién nos permite executar las sentencias de SQL

```python
try:
    # parametrso de la conexión
    # cursor_factory setea el tipo de cursor, en este caso para que nos devuelva el nombre de las columnas
    # elegimos RealDictCursor, y hay que importarlo.
    # from pyscopg2.extras import RealDictCursor
    conn = psycopg2.connect(host, database, user, password, cursor_factory=RealDictCursor)

    cursor = conn.cursor()
    print("Successfully connected to db")
except Exception as err:
    print(f"Connection failed with error: {err}")
```

## Interactuando con la base de datos

Ya configuramos la base de datos, tenemos nuestra conexión lista y nuestro cursor.
Refactoreemos los métodos GET y POST usando el cursor:

```python

class Post(BaseModel):
    title: str
    content: str
    

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # %s es para formatear el string y previene de SQL injection
    cursor.execute("INSERT INTO public.posts (title, content) VALUES(%s,%s) RETURNING *",
                   (post.title, post.content))
    new_post = cursor.fetchone()
    conn.commit()
    return {"message": new_post}
```