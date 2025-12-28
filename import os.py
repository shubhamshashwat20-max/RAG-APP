import os
import subprocess
import time
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from transformers import BlipProcessor, BlipForConditionalGeneration


QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "image_rag"


# ---------- PATCH 1: Auto-start Qdrant if not running ----------
def is_qdrant_running():
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((QDRANT_HOST, QDRANT_PORT))
    return result == 0


def start_qdrant_if_needed():
    if not is_qdrant_running():
        print("⚠️ Qdrant is NOT running. Starting local Qdrant Docker container...")
        try:
            subprocess.Popen(
                ["docker", "run", "-p", "6333:6333", "-p", "6334:6334", "qdrant/qdrant"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print("⏳ Waiting for Qdrant to start...")
            time.sleep(4)
        except Exception as e:
            print("❌ Failed to start Qdrant automatically. Error:", e)
            print("Please start Qdrant manually:")
            print("👉 docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant")
            exit()


start_qdrant_if_needed()


# ---------- Load Models ----------
caption_model = "Salesforce/blip-image-captioning-large"
processor = BlipProcessor.from_pretrained(caption_model)
captioner = BlipForConditionalGeneration.from_pretrained(caption_model)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")


# ---------- Connect to Qdrant ----------
try:
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
    client.get_collections()
    print("✅ Connected to Qdrant")
except Exception as e:
    print("❌ ERROR: Qdrant connection failed.")
    print("Reason:", e)
    print("\nMake sure Qdrant is running:")
    print("👉 docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant")
    exit()


# ---------- Create collection if not exists ----------
try:
    client.get_collection(COLLECTION_NAME)
    print(f"ℹ️ Collection '{COLLECTION_NAME}' already exists.")
except:
    print(f"🆕 Creating collection '{COLLECTION_NAME}'...")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=384, distance="Cosine")
