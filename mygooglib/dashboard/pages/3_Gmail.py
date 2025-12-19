import streamlit as st

from mygooglib import get_clients

st.set_page_config(page_title="Gmail | MyGoog", page_icon="📧")
st.title("📧 Gmail Composer")

clients = get_clients()

with st.form("email_form"):
    to = st.text_input("To")
    subject = st.text_input("Subject")
    body = st.text_area("Message Body", height=200)

    submitted = st.form_submit_button("Send Email")

    if submitted:
        if not to or not subject:
            st.warning("Please fill in 'To' and 'Subject'.")
        else:
            with st.spinner("Sending..."):
                try:
                    resp = clients.gmail.send_email(to=to, subject=subject, body=body)
                    msg_id = resp.get("id") if isinstance(resp, dict) else resp
                    st.success(f"Sent! Message ID: `{msg_id}`")
                except Exception as e:
                    st.error(f"Error sending email: {e}")
