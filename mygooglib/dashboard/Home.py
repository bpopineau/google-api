import datetime as dt

import streamlit as st

from mygooglib import get_clients

st.set_page_config(
    page_title="MyGoog Dashboard",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 MyGoog Automation Hub")
st.markdown("Your personal Google Workspace command center.")


@st.cache_resource
def get_cached_clients():
    return get_clients()


try:
    clients = get_cached_clients()
    st.success("✅ Authenticated with Google Services")
except Exception as e:
    st.error(f"Authentication failed: {e}")
    st.stop()

# --- Overview Stats ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📅 Calendar")
    now = dt.datetime.now()
    try:
        events = clients.calendar.list_events(time_min=now, max_results=5)
        if not events:
            st.info("No upcoming events.")
        else:
            for event in events:
                start = event.get("start", {}).get(
                    "dateTime", event.get("start", {}).get("date")
                )
                summary = event.get("summary", "No Title")
                st.write(f"**{summary}**")
                st.caption(f"{start}")
    except Exception as e:
        st.error(f"Error: {e}")

with col2:
    st.subheader("📝 Tasks")
    try:
        tasks = clients.tasks.list_tasks(show_completed=False, max_results=5)
        if not tasks:
            st.info("No pending tasks.")
        else:
            for t in tasks:
                st.write(f"☐ {t.get('title')}")
    except Exception as e:
        st.error(f"Error: {e}")

with col3:
    st.subheader("📂 Recent Drive Files")
    try:
        files = clients.drive.list_files(page_size=5)
        for f in files:
            st.write(f"📄 {f.get('name')}")
    except Exception as e:
        st.error(f"Error: {e}")
