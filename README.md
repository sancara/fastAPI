
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

## Intereactuando con la base de datos a través de ORM

Si bien con el código anterior logramos llegar a la base de datos e interactuar con ella, comunmente se utiliza un ORM.
En este código usarmos sqlalchemy. Lo que busca esta librería es tratar a las tablas y los datos que queremos ingresar, como objetos. Con lo cuál mediante métodos, armaremos la sentencia SQL

    pip install sqlalchemy

sqlalchemy no sabe como "hablar" con la base de datos, por lo tanto tenemos que armar la conexión.
creamos **database.py** para manejar la conexión:

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
db = os.getenv('DB_NAME')

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{db}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

ahora lo importante, las tablas, a las mismas se les llama modelos. Creamos un archivo llamado **models.py**
```python
from .database import Base
from sqlalchemy import Column, Integer, String


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
```

> Importante!!!
> hay que agregar lo siguiente al main.py
> "models.Base.metadata.create_all(bind=engine)"
> debemos importar models, engine, sessionlocal

nos falta desde el main, crear el tunel de conexión a la bd.

```python
# se agregan estos imports a los que teníamos
from sqlalchemy.orm import Session
from . import models
from . database import engine, SessionLocal
from fastapi import Depends


models.Base.metadata.create_all(bind=engine)

# también podríamos dejar esto en el database.py e importarlo
# conexión a la db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

crearemos un endpoint de prueba, para probar la conexión y la interacción mediante ORM
```python

@app.get("/sqlalchemy")
def get_post_db(db: Session = Depends(get_db)):
    return {"status": "Success"}
    
```

de esta manera, se crean las tablas, llegamos a nuestra bd a través del ORM.
¿Qué pasa si modificamos nuestra tabla y la misma ya está creada? SqlAlchemy no se ocupa de eso :sad:

## Cambios en los esquemas de las tablas ALEMBIC
