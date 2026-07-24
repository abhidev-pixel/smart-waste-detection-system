from database.database import (
    create_database,
    add_detection,
    get_all_detections,
    delete_detection
)
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from components.header import show_header
from components.sidebar import show_sidebar
from components.cards import dashboard_cards
from utils.mock_classifier import classify_waste

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

    records = get_all_detections()

    if not records:
        st.info("No detection records found.")
    else:
        for record in records[:5]:
            det_id, image_name, waste_type, confidence, detected_at = record
            st.write(f"🗂️ **{image_name}** → {waste_type} ({confidence*100:.1f}%) — {detected_at}")

elif page == "Upload Image":

    st.header("📤 Upload Waste Image")

    input_method = st.radio(
        "How would you like to provide the image?",
        ["Upload a file", "Use Camera"]
    )

    if input_method == "Upload a file":
        uploaded_file = st.file_uploader(
            "Choose an image",
            type=["jpg", "jpeg", "png"]
        )
    else:
        uploaded_file = st.camera_input("Take a photo")

    if uploaded_file:

        st.image(
            uploaded_file,
            caption="Uploaded Image",
            use_container_width=True
        )

        st.success("Image uploaded successfully!")

        if st.button("🔍 Classify Waste"):

            detections = classify_waste(uploaded_file.name)

            st.subheader("Predictions")

            for waste_type, confidence in detections:
                st.write(f"- **{waste_type}** ({confidence}%)")
                add_detection(uploaded_file.name, waste_type, confidence)

            st.success(f"✅ Saved {len(detections)} detection(s) to History!")

elif page == "Detection History":

    st.header("📊 Detection History")

    records = get_all_detections()

    if not records:
        st.info("No detection records found yet. Upload an image first!")
    else:
        st.caption(f"Showing {len(records)} record(s)")

        for record in records:
            det_id, image_name, waste_type, confidence, detected_at = record

            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.write(f"🗂️ **{image_name}**")
                st.caption(f"{waste_type} — {confidence}% — {detected_at}")

            with col3:
                if st.button("🗑️ Delete", key=f"delete_{det_id}"):
                    delete_detection(det_id)
                    st.rerun()

elif page == "Statistics":

    st.header("📈 Statistics Dashboard")

    records = get_all_detections()

    if not records:
        st.info("No data yet. Upload and classify some images first!")
    else:
        df = pd.DataFrame(
            records,
            columns=["id", "image_name", "waste_type", "confidence", "detected_at"]
        )

        st.subheader("Totals")
        st.metric("Total Detections", len(df))
        st.metric("Average Confidence", f"{df['confidence'].mean():.1f}%")

        st.subheader("Counts per Category")
        category_counts = df["waste_type"].value_counts()
        st.bar_chart(category_counts)

        st.subheader("Category Distribution")
        fig, ax = plt.subplots()
        ax.pie(category_counts, labels=category_counts.index, autopct="%1.1f%%")
        st.pyplot(fig)

        st.subheader("Detections Over Time")
        df["date"] = df["detected_at"].str[:10]
        daily_counts = df.groupby("date").size()
        st.line_chart(daily_counts)