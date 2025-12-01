import os
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

@st.cache_resource
def process_pdf(pdf_path):
    if not os.path.exists(pdf_path): return None
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages: text += page.extract_text() + "\n"
    chunks = [chunk.strip() for chunk in text.split('\n\n') if len(chunk) > 50]
    return chunks

def get_answer(user_query, chunks):
    if not chunks: return "Error: Knowledge Base empty.", 0.0
    
    documents = [user_query] + chunks
    tfidf_vectorizer = TfidfVectorizer().fit_transform(documents)
    cosine_similarities = cosine_similarity(tfidf_vectorizer[0:1], tfidf_vectorizer).flatten()
    
    # Get top match
    best_match_index = cosine_similarities.argsort()[:-5:-1][0]
    if best_match_index == 0: 
        best_match_index = cosine_similarities.argsort()[:-5:-1][1]
    
    score = cosine_similarities[best_match_index]
    
    if score < 0.1:
        return "I couldn't find exact information in the notes. Try rephrasing.", 0.0
        
    return chunks[best_match_index - 1], round(score * 100, 2)