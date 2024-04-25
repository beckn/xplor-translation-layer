from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union

import sys
sys.path.append('py/.')
from translation import *


app = FastAPI(
    title="Xplor",
    description="AI services for Xplor App",
    version="v0.0.1",
    contact={
        "name": "WITSLAB"
    },
    docs_url="/docs",
    redoc_url="/redocs",
    openapi_url="/api/v1/openapi.json",
    openapi_tags=[{"name": "healthcheck", "description": "Healthcheck operations"},
                  {"name": "translation", "description": "Translation operations"}]
)


current_datetime = datetime.now()
#################################################################################################################
#                                   Health Check                                                                #
#################################################################################################################
@app.get("/healthcheck", tags=["healthcheck"])
def health_check():
    """
    Health check endpoint to verify the status of the application.
    """
    
    return {"status": "ok"}


@app.get("/datecheck", tags=["healthcheck"])
def date_check():
    """
    Health check endpoint to verify the status of the application.
    """
    
    return {"date": current_datetime}

#################################################################################################################
#                                   Translate                                                                   #
#################################################################################################################
class TranslationRequest(BaseModel):
    text: Union[str, dict]
    from_ln: str
    to_ln: str


@app.post("/translate/", tags=["translation"])
def translate(request: TranslationRequest):
    """
    Translates the provided text from the source language to the target language.
    Accepts both plain text and JSON as input.
    """
    translated_text = translate_input(request.text, request.from_ln, request.to_ln)
    if isinstance(translated_text, str) and translated_text.startswith("Required translation package could not be installed"):
        raise HTTPException(status_code=500, detail="Translation package installation failed.")
    return {"translated_text": translated_text}