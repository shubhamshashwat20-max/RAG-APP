# backend.py
import os
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from transformers import BlipProcessor, BlipForConditionalGeneration
import uuid

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "image_rag"

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
captioner = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

try:
    client.get_collection(COLLECTION_NAME)
except:
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance="Cosine")
    )

def caption_image(img_path):
    image = Image.open(img_path).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    out = captioner.generate(**inputs, max_new_tokens=50)
    return processor.decode(out[0], skip_special_tokens=True)

def add_image_to_qdrant(img_path):
    caption = caption_image(img_path)
    embedding = embed_model.encode(caption).tolist()

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=str(uuid.uuid4()),
                vector=embedding,
                payload={
                    "image_path": img_path,
                    "caption": caption
                }
            )
        ]
    )

def query_images_by_text(text_query, top_k=5):
    query_embedding = embed_model.encode(text_query).tolist()
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k
    )

    return [{
        "score": r.score,
        "image": r.payload["image_path"],
        "caption": r.payload["caption"]
    } for r in results]
