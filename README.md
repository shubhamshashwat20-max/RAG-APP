# RAG-APP

# 🖼️ Image Retrieval Using Qdrant, BLIP & Sentence Transformers

This project implements a **Multimodal RAG pipeline** that allows you to:

- 📝 Auto-generate captions for images  
- 🔍 Convert captions into vector embeddings  
- 📦 Store them inside Qdrant Vector Database  
- 🔎 Search & retrieve images using natural text queries  

Powered by:
- **Salesforce BLIP** → Image captioning  
- **Sentence Transformers** → Text embeddings  
- **Qdrant** → Vector search  
- **Python** → Orchestration  

---

## 🚀 Features

### ✔ Automatic Image Captioning  
Uploads images and generates captions using **BLIP (BLIP Large)**.

### ✔ Text-to-Image Semantic Search  
Ask queries like *"mountains covered with clouds"* or *"dog running on grass"* and retrieve matching images.

### ✔ Vector Search Storage  
Captions are converted to text embeddings and stored inside **Qdrant**.

### ✔ CLI-based image search  
Search results show:
- Similarity score  
- Image path  
- Generated caption  

---

## 🛠️ Tech Stack

| Component | Technology |
|----------|------------|
| Captioning | BLIP (HuggingFace Transformers) |
| Embeddings | all-MiniLM-L6-v2 (Sentence Transformers) |
| Vector DB | Qdrant |
| Storage | Local file system |
| Language | Python |

---

## 📂 Project Structure

