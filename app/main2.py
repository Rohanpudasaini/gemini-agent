from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello")
async def hello_query(name: str):
    return {"message": f"Hello {name}"}

@app.get("/hello/{name}")
async def hello_path(name: str):
    return {"message": f"Hello {name}"}
