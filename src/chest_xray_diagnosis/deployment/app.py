from typing import Optional

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"messgae": "Hello World"}


@app.get("/Welcome")
def get_name(name: str):
    return {"name": name}


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8090, reload=True)

# ps -fA | grep python
