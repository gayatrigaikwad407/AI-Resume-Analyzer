# app.py
import streamlit as st
import pdfplumber
import spacy

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Resume analyzer function
def analyze_resume(file):
    with pdfplumber.open(file) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return {
        "Total Words": len(doc),
        "Named Entities (Top 10)": entities[:10]
    }

# Streamlit UI
st.title("🤖 AI Resume Analyzer")
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file:
    st.success("Resume Uploaded!")
    result = analyze_resume(uploaded_file)
    st.subheader("Extracted Info:")
    st.write(result)