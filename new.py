import streamlit as st
import pandas as pd

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Large CSV Search",
    layout="wide"
)

st.title("🔍 Large CSV Keyword Search (Chunked & Safe)")

CHUNK_SIZE = 100_000

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload large CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    # -------- READ HEADER ONLY --------
    uploaded_file.seek(0)
    header_df = pd.read_csv(uploaded_file, nrows=0)
    header_df.columns = header_df.columns.str.strip()
    columns = header_df.columns.tolist()

    # -------- PREVIEW FIRST ROWS --------
    uploaded_file.seek(0)
    preview_df = pd.read_csv(uploaded_file, nrows=50)

    st.subheader("📄 CSV Preview (First 50 Rows)")
    st.dataframe(preview_df, use_container_width=True)

    # -------- SEARCH CONTROLS --------
    st.subheader("🔎 Search Options")

    column_to_search = st.selectbox(
        "Select column to search",
        columns
    )

    keyword = st.text_input(
        "Enter keyword (case-insensitive)"
    )

    # -------- SEARCH BUTTON --------
    if st.button("Search") and keyword.strip():

        st.info("🔄 Searching CSV in chunks...")

        uploaded_file.seek(0)

        matched_chunks = []
        total_matches = 0

        for chunk in pd.read_csv(uploaded_file, chunksize=CHUNK_SIZE):
            chunk.columns = chunk.columns.str.strip()

            if column_to_search not in chunk.columns:
                st.error(
                    f"❌ Column '{column_to_search}' not found in file"
                )
                st.stop()

            # Safe string conversion
            chunk[column_to_search] = chunk[column_to_search].astype(str)

            matched = chunk[
                chunk[column_to_search]
                .str.contains(keyword, case=False, na=False)
            ]

            if not matched.empty:
                matched_chunks.append(matched)
                total_matches += len(matched)

        # -------- RESULTS --------
        if matched_chunks:
            result_df = pd.concat(
                matched_chunks,
                ignore_index=True
            )

            st.success(
                f"✅ Found {total_matches} matching rows"
            )

            st.subheader("📊 Search Results (Preview)")
            st.dataframe(
                result_df.head(500),
                use_container_width=True
            )

            st.download_button(
                label="⬇️ Download full results (CSV)",
                data=result_df.to_csv(index=False),
                file_name="search_results.csv",
                mime="text/csv"
            )
        else:
            st.warning("❌ No matches found")

# ---------------- FOOTER ----------------
st.markdown(
    "---\n"
    "⚡ Optimized for large CSV files | Chunked processing | Safe preview"
)
