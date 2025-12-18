import os

import streamlit as st

from mygooglib import get_clients

st.set_page_config(page_title="Drive | MyGoog", page_icon="📂")
st.title("📂 Google Drive Explorer")

clients = get_clients()

# --- Upload Section ---
with st.expander("Upload File"):
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file:
        if st.button("Upload to Drive"):
            with st.spinner("Uploading..."):
                # Save temp to upload
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                try:
                    file_id = clients.drive.upload_file(
                        temp_path, name=uploaded_file.name
                    )
                    st.success(f"Uploaded! ID: `{file_id}`")
                except Exception as e:
                    st.error(f"Failed: {e}")
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

# --- Browser Section ---
st.subheader("Brose Files")
query = st.text_input("Search", placeholder="Name contains...")
if st.button("Search") or query:
    q_str = f"name contains '{query}'" if query else None
    files = clients.drive.list_files(query=q_str, page_size=20)

    if not files:
        st.info("No files found.")
    else:
        for f in files:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📄 **{f['name']}**")
                st.caption(f"ID: {f['id']}")
            with col2:
                # Placeholder for actions like Download
                st.button("Info", key=f["id"], help=f"MIME: {f.get('mimeType')}")
