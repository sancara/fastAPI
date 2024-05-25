
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