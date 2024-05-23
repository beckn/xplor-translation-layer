from fastapi import FastAPI, HTTPException, Depends, Security, Request
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader, APIKey
from typing import Dict, List
from hashlib import sha256
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Union

import sys
sys.path.append('src/py/.')
from translation import *
from rec_sys import *


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
    openapi_tags=[{"name": "Healthcheck", "description": "Healthcheck operations"},
                  {"name": "Translation", "description": "Translation operations"},
                  {"name": "Rec_Sys", "description": "Recommender System"}]
)


current_datetime = datetime.now()
# Define your private key (keep it secret)
PRIVATE_KEY = "da98faf9sf3qF0A9FSAsdfadsf5sdf78f90as0f8df6dsg432f32s5D8F7SA9DR6G485"
#################################################################################################################
#                                   Health Check                                                                #
#################################################################################################################
@app.get("/healthcheck", tags=["Healthcheck"])
def health_check():
    """
    Health check endpoint to verify the status of the application.
    """
    
    return {"status": "ok"}


@app.get("/datecheck", tags=["Healthcheck"])
def date_check():
    """
    Health check endpoint to verify the status of the application.
    """
    
    return {"date": current_datetime}


#################################################################################################################
#                                   Authentication                                                              #
#################################################################################################################


# Function to generate API key dynamically
def generate_api_key(user_id: str) -> str:
    concatenated_key = f"{user_id}-{PRIVATE_KEY}"
    hashed_key = sha256(concatenated_key.encode()).hexdigest()
    return hashed_key

# Function to validate API key
def validate_api_key(user_id: str, api_key: str) -> bool:
    return api_key == generate_api_key(user_id)


# Dependency to validate API key
def check_api_key( user_id: str, api_key: str) -> Dict[str, str]:
    if validate_api_key( user_id, api_key):
        return {"user_id": user_id, "api_key": api_key}
    else:
        raise HTTPException(status_code=403, detail="Invalid API key")


# Route to generate API key dynamically
@app.get("/generate-api-key/{user_id}",tags=["Authorisation"], include_in_schema=False)
async def generate_api_key_route(user_id: str):
    api_key = generate_api_key(user_id)
    return {"user_id": user_id, "api_key": api_key}
#################################################################################################################
#                                   Translate                                                                   #
#################################################################################################################

@app.get("/supported_languages", tags=["Translation"])
#def get_supported_languages(credentials: Dict[str, str] = Depends(check_api_key)):
def get_supported_languages():
    """
    Endpoint to get the list of all supported languages along with their ISO codes.
    """
    from src.py.utils import argos_languages, bhashini_languages
    supported_languages = {**argos_languages, **bhashini_languages}
    return {"supported_languages": supported_languages}


################################################################################################################
class TranslationRequest(BaseModel):
    text: Union[str, Dict[str, str], List[Union[str, Dict[str, str]]]]
    from_ln: str
    to_ln: str


@app.post("/translate/", tags=["Translation"])
#def translate(request: TranslationRequest, credentials: Dict[str, str] = Depends(check_api_key)):
def translate(request: TranslationRequest):
    """
    Translates the provided text from the source language to the target language.
    Accepts both plain text and JSON as input.
    """
    translated_text = translate_input(request.text, request.from_ln, request.to_ln)
    if isinstance(translated_text, str) and translated_text.startswith("Required translation package could not be installed"):
        raise HTTPException(status_code=500, detail="Translation package installation failed.")
    return {"translated_text": translated_text}

#################################################################################################################
#                                   RecSys                                                                      #
#################################################################################################################

class RecsysRequest(BaseModel):
    text: dict
    type: str


@app.post("/recsys/", tags=["Rec_Sys"])
#def recsys_route(request: RecsysRequest, credentials: Dict[str, str] = Depends(check_api_key)):
def recsys_route(request: RecsysRequest):
    """
    Translates the provided text from the source language to the target language.
    Accepts both plain text and JSON as input.
    """
    recsys_op = rec_sys_input(request.text, request.type)
    return recsys_op.to_dict()