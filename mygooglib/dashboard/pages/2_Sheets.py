import streamlit as st

from mygooglib import get_clients

st.set_page_config(page_title="Sheets | MyGoog", page_icon="📊")
st.title("📊 Sheets Viewer")

clients = get_clients()

sheet_id = st.text_input("Spreadsheet ID or URL")
range_name = st.text_input("Range (e.g. Sheet1!A1:Z)")

if st.button("Load Data"):
    if not sheet_id or not range_name:
        st.warning("Please provide ID and Range.")
    else:
        with st.spinner("Loading from Sheets..."):
            try:
                df = clients.sheets.to_dataframe(sheet_id, range_name)
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error loading sheet: {e}")
