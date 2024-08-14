from fastapi import FastAPI
from langserve import add_routes # fastapi
import helpers

app = FastAPI()

@app.get('/')
def home_page():
    return {"hello": "world"}

chain = helpers.get_chain()

add_routes(
    app,
    chain,
    path='/chain'
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8100)