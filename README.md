# FastAPI Learning Repository

## Setup and Installation

1. Create a virtual environment using `uv`:

```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

2. Install required dependencies:

```bash
# uv pip install 'fastapi[all]'
uv add 'fastapi[all]'
```

Both commands work, but `uv add` is the preferred way as it's faster and handles dependencies more efficiently than `uv pip install`.

## Basic FastAPI Application

Here's our first FastAPI application (`main.py`):

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

Let's break down each part:

- `from fastapi import FastAPI`: Imports the FastAPI class
- `app = FastAPI()`: Creates an instance of the FastAPI application
- `@app.get("/")`: Decorator that tells FastAPI this function handles GET requests at the root path "/"
- `async def root()`: Defines an asynchronous function that handles the request
- `return {"message": "Hello World"}`: Returns a JSON response

To run the application:

```bash
uvicorn main:app --reload
```

The `--reload` flag enables auto-reload during development when code changes are detected.
