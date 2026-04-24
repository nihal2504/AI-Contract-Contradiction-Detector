import streamlit as st
import pandas as pd
from pypdf import PdfReader

from src.clause_splitter import split_clauses
from src.pair_generator import generate_pairs
from src.contradiction_detector import detect_contradictions

st.set_page_config(page_title="Contract Contradiction Detector", layout="wide")

st.title("AI Contract Contradiction Detector")
st.write("Upload a contract and detect contradictory clauses using DeBERTa-based Natural Language Inference.")

uploaded = st.file_uploader("Upload contract file", type=["txt", "pdf"])

threshold = st.slider("Contradiction threshold", 0.1, 0.95, 0.65, 0.05)
top_k = st.slider("Number of candidate pairs", 5, 100, 30, 5)

def read_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
        text += "\n"
    return text

if uploaded:
    if uploaded.name.endswith(".pdf"):
        text = read_pdf(uploaded)
    else:
        text = uploaded.read().decode("utf-8")

    clauses = split_clauses(text)

    st.subheader("Extracted Clauses")
    st.write(f"Total clauses found: {len(clauses)}")
    st.dataframe(pd.DataFrame(clauses), use_container_width=True)

    if st.button("Detect Contradictions"):
        pairs = generate_pairs(clauses, top_k=top_k)
        results = detect_contradictions(pairs, threshold=threshold)

        st.subheader("Contradiction Report")

        if results:
            df = pd.DataFrame(results)
            st.metric("Contradictions Found", len(results))
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download CSV Report",
                csv,
                "contract_contradiction_report.csv",
                "text/csv"
            )
        else:
            st.success("No strong contradictions found at this threshold.")