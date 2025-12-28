<<<<<<< HEAD
import os
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from transformers import BlipProcessor, BlipForConditionalGeneration

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "image_rag"


caption_model = "Salesforce/blip-image-captioning-large"
processor = BlipProcessor.from_pretrained(caption_model)
captioner = BlipForConditionalGeneration.from_pretrained(caption_model)

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
    image = Image.open(img_path)
    inputs = processor(image, return_tensors="pt").to("cpu")
    out = captioner.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption


def add_image_to_qdrant(img_path, point_id):
    caption = caption_image(img_path)
    embedding = embed_model.encode(caption).tolist()

    payload = {
        "image_path": img_path,
        "caption": caption,
    }

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=point_id,      
                vector=embedding,
                payload=payload
            )
        ]
    )

    print(f"Added: {img_path} | Caption: {caption}")


def query_images_by_text(text_query, top_k=5):
    query_embedding = embed_model.encode(text_query).tolist()

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k
    )

    output = []
    for r in results:
        output.append({
            "score": r.score,
            "image": r.payload["image_path"],
            "caption": r.payload["caption"]
        })

    return output


if __name__ == "__main__":



    folder = "C:\\Users\\Shubham\\OneDrive\\Desktop\\Mussorie Photos"

    
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created folder: {folder}. Please add images inside it and rerun the script.")
        exit()  

    print("\n=== Adding images to vector DB ===")
    for idx, file in enumerate(os.listdir(folder), start=1):
        if file.lower().endswith(("png", "jpg", "jpeg", "webp")):
            add_image_to_qdrant(os.path.join(folder, file), point_id=idx)

    print("\n=== Query Images ===")
    query = input("Enter search text: ")
    res = query_images_by_text(query)

    print("\nResults:")
    for r in res:
        print(f"- {r['image']}  | score={r['score']:.4f}")
        print(f"  caption → {r['caption']}")
=======
import os
from PIL import Image
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from transformers import BlipProcessor, BlipForConditionalGeneration

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "image_rag"


caption_model = "Salesforce/blip-image-captioning-large"
processor = BlipProcessor.from_pretrained(caption_model)
captioner = BlipForConditionalGeneration.from_pretrained(caption_model)

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
    image = Image.open(img_path)
    inputs = processor(image, return_tensors="pt").to("cpu")
    out = captioner.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption


def add_image_to_qdrant(img_path, point_id):
    caption = caption_image(img_path)
    embedding = embed_model.encode(caption).tolist()

    payload = {
        "image_path": img_path,
        "caption": caption,
    }

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=point_id,      
                vector=embedding,
                payload=payload
            )
        ]
    )

    print(f"Added: {img_path} | Caption: {caption}")


def query_images_by_text(text_query, top_k=5):
    query_embedding = embed_model.encode(text_query).tolist()

    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_embedding,
        limit=top_k
    )

    output = []
    for r in results:
        output.append({
            "score": r.score,
            "image": r.payload["image_path"],
            "caption": r.payload["caption"]
        })

    return output


if __name__ == "__main__":

    
    folder = "images"

    
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Created folder: {folder}. Please add images inside it and rerun the script.")
        exit()  

    print("\n=== Adding images to vector DB ===")
    for idx, file in enumerate(os.listdir(folder), start=1):
        if file.lower().endswith(("png", "jpg", "jpeg", "webp")):
            add_image_to_qdrant(os.path.join(folder, file), point_id=idx)

    print("\n=== Query Images ===")
    query = input("Enter search text: ")
    res = query_images_by_text(query)

    print("\nResults:")
    for r in res:
        print(f"- {r['image']}  | score={r['score']:.4f}")
        print(f"  caption → {r['caption']}")
>>>>>>> 55e424f90b793f813132b0aefd6c3f1bcb256ebc
