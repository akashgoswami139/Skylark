from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from agent import Agent   # use "from pipeline import Agent" if the file is still pipeline.py

app = FastAPI()

class Query(BaseModel):
    city: str
    mode: str   # "weather" or "city"

@app.post("/api/agent")
def ask(q: Query):
    if q.mode == "weather":
        prompt = f"What is the weather of {q.city}?"
    else:
        prompt = f"Tell me about the city {q.city}"
    try:
        return {"answer": Agent(prompt).run()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Must stay last, so it doesn't swallow the /api route
app.mount("/", StaticFiles(directory=".", html=True), name="ui")