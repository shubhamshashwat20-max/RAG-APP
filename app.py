# app.py
import streamlit as st
from backend import query_images_by_text
from PIL import Image

st.set_page_config(
    page_title="Image RAG AI",
    layout="wide"
)

st.title("🖼️ Image RAG AI")
st.write("Search images using **natural language**")

query = st.text_input(
    "🔍 Enter your search query",
    placeholder="e.g. dog playing on grass"
)

if query:
    with st.spinner("Searching images..."):
        results = query_images_by_text(query, top_k=5)

    if results:
        cols = st.columns(len(results))
        for col, res in zip(cols, results):
            with col:
                img = Image.open(res["image"])
                st.image(img, use_column_width=True)
                st.caption(res["caption"])
                st.text(f"Score: {res['score']:.3f}")
    else:
        st.warning("No matching images found.")
