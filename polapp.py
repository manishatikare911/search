import streamlit as st
import polars as pl

st.set_page_config(page_title="Large CSV Search (Polars)", layout="wide")
st.title("🔍 Large CSV Keyword Search (Polars)")

uploaded_file = st.file_uploader(
    "Upload CSV file (1GB+ supported)",
    type=["csv"]
)

if uploaded_file:
    st.info("File uploaded successfully. Polars will stream the data.")

    # Read CSV lazily (NO full load)
    lf = pl.scan_csv(uploaded_file)

    st.success("CSV schema loaded (lazy mode).")

    # Show columns
    columns = lf.columns
    column_to_search = st.selectbox("Select column to search", columns)

    keyword = st.text_input("Enter keyword")

    max_rows = st.number_input(
        "Max rows to display",
        min_value=10,
        max_value=5000,
        value=500
    )

    if st.button("Search") and keyword:
        with st.spinner("Searching (streaming)…"):
            # Convert column to string and filter
            result = (
                lf.with_columns(
                    pl.col(column_to_search).cast(pl.Utf8)
                )
                .filter(
                    pl.col(column_to_search)
                    .str.contains(keyword, literal=False)
                )
                .limit(max_rows)
                .collect(streaming=True)
            )

        st.success(f"Found {result.height} matching rows (showing max {max_rows})")
        st.dataframe(result.to_pandas())

