from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from qdrant_client import models, QdrantClient
from pydantic import BaseModel
from typing import Union
from server.data import encoder
import os

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
client = QdrantClient(url=QDRANT_URL)
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
    for key , value in filters_dict.items():
        if value:
            condition = models.FieldCondition(
                        key=key,
                        match=models.MatchValue(value=value),
                    )
            field_conditions.append(condition)

    results = client.search(
        collection_name="mori_collection",
        query_vector = text_encoded_vector,
        query_filter=models.Filter( must = field_conditions)
    )

    return {"results": results}
