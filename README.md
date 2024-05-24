
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