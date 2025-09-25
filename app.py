import streamlit as st
import pandas as pd

st.title("🔍 CSV Keyword Search App")

# Upload CSV file
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Read CSV into DataFrame
    df = pd.read_csv(uploaded_file)
    st.write("📊 Preview of Uploaded Data:")
    st.dataframe(df)

    # Select column to search
    column_to_search = st.selectbox("Select column to search", df.columns)

    # Search box
    keyword = st.text_input("Enter keyword to search")

    if keyword:
        # Filter rows containing the keyword (case-insensitive)
        filtered_df = df[df[column_to_search].astype(str).str.contains(keyword, case=False, na=False)]

        st.write(f"🔎 Results for '{keyword}' in column '{column_to_search}':")
        st.dataframe(filtered_df)

        st.success(f"Found {len(filtered_df)} matching row(s).")
