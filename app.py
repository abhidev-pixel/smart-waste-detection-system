from database.database import create_database
import streamlit as st

from components.header import show_header
from components.sidebar import show_sidebar
from components.cards import dashboard_cards

create_database()


# ------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------

st.set_page_config(
    page_title="Smart Waste Detection System",
    page_icon="♻️",
    layout="wide"
)

# ------------------------------------------------
# HEADER
# ------------------------------------------------

show_header()

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

page = show_sidebar()

# ------------------------------------------------
# PAGE CONTENT
# ------------------------------------------------

if page == "Dashboard":

    st.divider()

    dashboard_cards()

    st.subheader("📋 Recent Activity")

    st.info("No detection records found.")

elif page == "Upload Image":

    st.header("📤 Upload Waste Image")

    uploaded_file = st.file_uploader(
        "Choose an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        st.image(
            uploaded_file,
            caption="Uploaded Image",
            use_container_width=True
        )

elif page == "Detection History":

    st.header("📜 Detection History")

    st.info("Database integration will be added in Phase 3.")

elif page == "Statistics":

    st.header("📊 Statistics")

    st.info("Charts will be available after AI integration.")

elif page == "About":

    st.header("ℹ️ About")

    st.write("""
    **Smart Waste Detection and Classification System**

    Developed using:

    - Python
    - Streamlit
    - OpenCV
    - SQLite
    - Computer Vision
    """)