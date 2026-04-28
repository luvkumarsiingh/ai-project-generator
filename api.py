from fastapi import FastAPI
from pydantic import BaseModel
from graph import app

app_api = FastAPI()

class Request(BaseModel):
    prompt: str

@app_api.post("/generate")
def generate(req: Request):
    result = app.invoke({
        "user_prompt": req.prompt
    })

    return {"status": "done"}