import streamlit as st
import pandas as pd

st.set_page_config(page_title="Large CSV Search", layout="wide")
st.title("🔍 Large CSV Keyword Search (Chunked)")

uploaded_file = st.file_uploader("Upload large CSV", type=["csv"])
CHUNK_SIZE = 100_000

if uploaded_file is not None:
    # 🔹 Read header only
    uploaded_file.seek(0)
    header_df = pd.read_csv(uploaded_file, nrows=0)

    # 🔹 Normalize column names
    header_df.columns = header_df.columns.str.strip()
    columns = header_df.columns.tolist()

    column_to_search = st.selectbox("Select column to search", columns)
    keyword = st.text_input("Enter keyword")

    if st.button("Search") and keyword:
        st.info("🔄 Searching CSV in chunks...")

        uploaded_file.seek(0)  # 🔥 CRITICAL FIX

        matched_chunks = []
        total_matches = 0

        for chunk in pd.read_csv(uploaded_file, chunksize=CHUNK_SIZE):
            # 🔹 Normalize chunk column names
            chunk.columns = chunk.columns.str.strip()

            if column_to_search not in chunk.columns:
                st.error(f"❌ Column '{column_to_search}' not found in chunk")
                st.stop()

            # 🔹 Safe string conversion
            chunk[column_to_search] = chunk[column_to_search].astype(str)

            matched = chunk[
                chunk[column_to_search]
                .str.contains(keyword, case=False, na=False)
            ]

            if not matched.empty:
                matched_chunks.append(matched)
                total_matches += len(matched)

        if matched_chunks:
            result_df = pd.concat(matched_chunks, ignore_index=True)

            st.success(f"✅ Found {total_matches} matching rows")
            st.dataframe(result_df.head(500))

            st.download_button(
                "⬇️ Download results",
                result_df.to_csv(index=False),
                "search_results.csv",
                "text/csv"
            )
        else:
            st.warning("❌ No matches found")
