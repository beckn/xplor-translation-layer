from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union
from py.translation import *

app = FastAPI(
    title="Xplor",
    description="AI services for Xplor App",
    version="1.0.0",
    contact={
        "name": "WITSLAB"
    },
    docs_url="/docs",
    redoc_url="/redocs",
    openapi_url="/api/v1/openapi.json",
    openapi_tags=[{"name": "translation", "description": "Translation operations"}]
)


class TranslationRequest(BaseModel):
    text: Union[str, dict]
    from_ln: str
    to_ln: str


@app.post("/translate/")
def translate(request: TranslationRequest):
    """
    Translates the provided text from the source language to the target language.
    Accepts both plain text and JSON as input.
    """
    translated_text = translate_input(request.text, request.from_ln, request.to_ln)
    if isinstance(translated_text, str) and translated_text.startswith("Required translation package could not be installed"):
        raise HTTPException(status_code=500, detail="Translation package installation failed.")
    return {"translated_text": translated_text}