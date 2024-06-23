from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Union
import requests
import os
from server.data import encoder  # Assuming this contains your encoder function

QDRANT_URL = os.getenv("QDRANT_URL", "https://qdrant.darkube.app/")
app = FastAPI()

# CORS middleware configuration
origins = ["*"]  # Adjust as per your frontend URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class Filters(BaseModel):
    brand_name: str | None = None
    category_name: str | None = None
    shop_name: str | None = None

@app.post("/search/")
async def search(text: str , filters: Filters | None = None):
    text_encoded_vector = encoder.encode_text(text).cpu().numpy().tolist()[0]

    field_conditions = []
    filters_dict = filters.dict() if filters is not None else {}
    for key, value in filters_dict.items():
        if value:
            condition = {
                "key": key,
                "match": {
                    "value": value
                }
            }
            field_conditions.append(condition)

    payload = {
        "filter": {
            "must": field_conditions
        },
        "vector": text_encoded_vector,
        "with_payload": True,
        "score_threshold":0.25,
        "limit": 15
    }

    url = f"{QDRANT_URL}/collections/mori_collection/points/search"

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        results = response.json()
        return {"results": results}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to perform search query: {str(e)}")
