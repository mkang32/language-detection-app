from fastapi import FastAPI
from pydantic import BaseModel
from app.model.model import predict_pipeline
from app.model.model import __version__ as model_version

app = FastAPI()


class TextIn(BaseModel):
    text: str


class PredictionOut(BaseModel):
    language: str
    probability: float


@app.get("/")
def home():
    return {"health_check": "OK", "model_version": model_version}


@app.post("/predict", response_model=PredictionOut)
def predict(payload: TextIn):
    language, prob = predict_pipeline(payload.text)
    return {"language": language, "probability": prob}
