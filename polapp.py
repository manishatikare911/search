# import streamlit as st
# import polars as pl

# st.set_page_config(page_title="Large CSV Search (Polars)", layout="wide")
# st.title("🔍 Large CSV Keyword Search (Polars)")

# uploaded_file = st.file_uploader(
#     "Upload CSV file (1GB+ supported)",
#     type=["csv"]
# )

# if uploaded_file:
#     st.info("File uploaded successfully. Polars will stream the data.")

#     # Read CSV lazily (NO full load)
#     lf = pl.scan_csv(uploaded_file)

#     st.success("CSV schema loaded (lazy mode).")

#     # Show columns
#     columns = lf.columns
#     column_to_search = st.selectbox("Select column to search", columns)

#     keyword = st.text_input("Enter keyword")

#     max_rows = st.number_input(
#         "Max rows to display",
#         min_value=10,
#         max_value=5000,
#         value=500
#     )

#     if st.button("Search") and keyword:
#         with st.spinner("Searching (streaming)…"):
#             # Convert column to string and filter
#             result = (
#                 lf.with_columns(
#                     pl.col(column_to_search).cast(pl.Utf8)
#                 )
#                 .filter(
#                     pl.col(column_to_search)
#                     .str.contains(keyword, literal=False)
#                 )
#                 .limit(max_rows)
#                 .collect(streaming=True)
#             )

#         st.success(f"Found {result.height} matching rows (showing max {max_rows})")
#         st.dataframe(result.to_pandas())
import streamlit as st
import pandas as pd

st.set_page_config(page_title="CSV Keyword Search", layout="wide")
st.title("🔍 Large CSV Keyword Search (Chunked)")

uploaded_file = st.file_uploader("Upload your CSV file (Large files supported)", type=["csv"])

CHUNK_SIZE = 100_000   # adjust based on RAM

if uploaded_file is not None:
    # Read only header first
    df_head = pd.read_csv(uploaded_file, nrows=0)
    columns = df_head.columns.tolist()

    column_to_search = st.selectbox("Select column to search", columns)
    keyword = st.text_input("Enter keyword to search")

    if st.button("Search") and keyword:
        st.info("🔄 Searching CSV in chunks... Please wait")

        matched_chunks = []
        total_matches = 0

        progress = st.progress(0)
        chunk_count = 0

        for chunk in pd.read_csv(uploaded_file, chunksize=CHUNK_SIZE):
            chunk_count += 1

            # PyArrow safety
            if chunk[column_to_search].dtype == "object":
                chunk[column_to_search] = chunk[column_to_search].astype(str)

            matched = chunk[
                chunk[column_to_search]
                .str.contains(keyword, case=False, na=False)
            ]

            if not matched.empty:
                matched_chunks.append(matched)
                total_matches += len(matched)

            progress.progress(min(chunk_count / 100, 1.0))

        if matched_chunks:
            result_df = pd.concat(matched_chunks, ignore_index=True)

            st.success(f"✅ Found {total_matches} matching rows")
            st.dataframe(result_df.head(500))  # show only first 500 rows

            # Optional download
            st.download_button(
                "⬇️ Download results as CSV",
                result_df.to_csv(index=False),
                file_name="search_results.csv",
                mime="text/csv"
            )
        else:
            st.warning("❌ No matches found")

