from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from transformers import AutoTokenizer, AutoModel
import torch
import os

class EmbeddingModel:
    def __init__(self, model_name="intfloat/multilingual-e5-large", cache_dir="./cache"):
        self.cache_dir = cache_dir
        self.model_name = model_name

        # 檢查模型是否已下載，如果未下載則下載模型
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        self._ensure_model_downloaded()

        self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=self.cache_dir)
        self.model = AutoModel.from_pretrained(model_name, cache_dir=self.cache_dir)

    def _ensure_model_downloaded(self):
        # 預先下載模型
        try:
            AutoTokenizer.from_pretrained(self.model_name, cache_dir=self.cache_dir)
            AutoModel.from_pretrained(self.model_name, cache_dir=self.cache_dir)
        except Exception as e:
            print(f"Error downloading model {self.model_name}: {e}")
            raise

    def get_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

app = FastAPI()
embedding_model = EmbeddingModel()

class EmbeddingRequest(BaseModel):
    input: List[str]
    model: str = "intfloat/multilingual-e5-large"

class EmbeddingResponse(BaseModel):
    object: str = "embedding"
    data: List[dict]
    model: str
    usage: dict

@app.post("/v1/embeddings", response_model=EmbeddingResponse)
async def create_embeddings(request: EmbeddingRequest):
    if not request.input:
        raise HTTPException(status_code=400, detail="Input text cannot be empty")
    
    embeddings = []
    for idx, text in enumerate(request.input):
        embedding_vector = embedding_model.get_embedding(text).tolist()
        embeddings.append({
            "object": "embedding",
            "embedding": embedding_vector,
            "index": idx
        })
    
    response = EmbeddingResponse(
        data=embeddings,
        model=request.model,
        usage={
            "prompt_tokens": sum(len(text.split()) for text in request.input),
            "total_tokens": sum(len(text.split()) for text in request.input)
        }
    )
    return response
