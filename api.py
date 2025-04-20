from fastapi import FastAPI
from agent import getMovieDetails

app = FastAPI()

# FastAPI endPoint
@app.get("/getMovieDetails")
async def getMovieDetails_endpoint(q:str | None = None, model:str | None = None):
    return await getMovieDetails(q, model)

