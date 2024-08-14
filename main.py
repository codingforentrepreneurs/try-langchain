from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from langserve import add_routes # fastapi
import helpers
from decouple import config
from redis import Redis

app = FastAPI()
redis_instance = Redis(
  host=config("REDIS_HOST", cast=str),
  port=config("REDIS_PORT", cast=int, default=6379),
  password=config("REDIS_PASSWORD", cast=str),
  ssl=True
)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    rate_limit = 5
    rate_window = 10 # seconds
    visits_key = "visits"
    current_val = redis_instance.get(visits_key)
    if current_val is None:
        redis_instance.set(visits_key, 0, rate_window)
    redis_instance.incr(visits_key)
    final_val = redis_instance.get(visits_key)
    do_rate_limiting = False 
    try:
        do_rate_limiting = int(final_val) > rate_limit
    except:
        pass
    if do_rate_limiting:
        return JSONResponse(content={"error": "Rate Limited"},status_code=429)
    response = await call_next(request)
    return response

@app.get('/')
def home_page():
    
    return {"hello": "world"}

chain = helpers.get_chain()

# /chain/playground/
# /chain/invoke
# /chain/stream
# /chain/batch

add_routes(
    app,
    chain,
    path='/chain'
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8100)