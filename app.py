import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from database.database import (
    create_database,
    add_detection,
    get_all_detections,
    delete_detection
)
from components.sidebar import show_sidebar
from components.cards import dashboard_cards

# Real model integration check with graceful fallback
try:
    from detection.detector import classify_waste
except ImportError:
    from utils.mock_classifier import classify_waste

create_database()

# ------------------------------------------------
# PAGE CONFIGURATION
# ------------------------------------------------
st.set_page_config(
    page_title="Smart Waste AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------
# APPLE DESIGN SYSTEM (CSS)
# ------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", sans-serif !important;
        -webkit-font-smoothing: antialiased;
    }

    .stApp {
        background-color: #000000 !important;
        color: #F5F5F7 !important;
    }

    /* Apple Glass Cards */
    .metric-card {
        background: rgba(28, 28, 30, 0.65) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 18px !important;
        padding: 24px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5) !important;
        backdrop-filter: blur(20px) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.1, 0.25, 1) !important;
    }

    .metric-card:hover {
        transform: scale(1.02);
        border-color: rgba(255, 255, 255, 0.25) !important;
    }

    .metric-label {
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: #86868B !important;
        margin-bottom: 6px !important;
    }

    .metric-value {
        font-size: 2.4rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        color: #F5F5F7 !important;
    }

    /* Apple-Style Buttons */
    .stButton > button {
        background: #0071E3 !important;
        color: #FFFFFF !important;
        font-weight: 500 !important;
        font-size: 0.95rem !important;
        border-radius: 980px !important;
        padding: 0.55rem 1.6rem !important;
        border: none !important;
        transition: all 0.2s cubic-bezier(0.25, 0.1, 0.25, 1) !important;
        box-shadow: 0 4px 12px rgba(0, 113, 227, 0.3) !important;
    }

    .stButton > button:hover {
        background: #0077ED !important;
        transform: scale(1.03) !important;
        box-shadow: 0 6px 16px rgba(0, 113, 227, 0.45) !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #161617 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }

    /* Custom List Item Cards for Activity */
    .activity-row {
        background: rgba(28, 28, 30, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px 18px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Hide Default Header Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# HERO BANNER
# ------------------------------------------------
st.markdown("""
    <div style="background: radial-gradient(circle at top left, rgba(0,113,227,0.15), rgba(0,0,0,0) 60%); 
                padding: 2.2rem; border-radius: 22px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 2rem;">
        <h1 style="margin:0; font-size: 2.6rem; color: #F5F5F7; font-weight: 700; letter-spacing: -0.03em;">
            Smart Waste <span style="color:#2997FF;">Detection System</span>
        </h1>
        <p style="margin-top: 0.5rem; color: #86868B; font-size: 1.05rem; font-weight: 400;">
            Real-time automated waste classification and telemetry powered by computer vision.
        </p>
    </div>
""", unsafe_allow_html=True)

page = show_sidebar()

# ------------------------------------------------
# HELPER PARSER
# ------------------------------------------------
def parse_record(record):
    if isinstance(record, dict):
        return (
            record.get("id"),
            record.get("image_name"),
            record.get("waste_type"),
            float(record.get("confidence", 0.0)),
            record.get("detected_at") or record.get("timestamp", "")
        )
    return (
        record[0],
        record[1],
        record[2],
        float(record[3]),
        record[4]
    )

# ------------------------------------------------
# PAGE CONTENT
# ------------------------------------------------
if page == "Dashboard":

    dashboard_cards()
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Recent Detections")

    records = get_all_detections()

    if not records:
        st.info("No detection records found.")
    else:
        for record in records[:5]:
            det_id, image_name, waste_type, confidence, detected_at = parse_record(record)
            conf_pct = confidence * 100 if confidence <= 1.0 else confidence
            
            st.markdown(f"""
                <div class="activity-row">
                    <div>
                        <span style="font-weight: 600; color: #F5F5F7;">📄 {image_name}</span>
                        <span style="color: #86868B; margin-left: 10px;">• {detected_at}</span>
                    </div>
                    <div>
                        <span style="background: rgba(41, 151, 255, 0.15); color: #2997FF; padding: 4px 12px; border-radius: 980px; font-size: 0.85rem; font-weight: 500;">
                            {waste_type.title()} ({conf_pct:.1f}%)
                        </span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

elif page == "Upload Image":

    st.header("Upload Waste Image")

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

        if st.button("Classify Waste"):

            predictions = classify_waste(uploaded_file)
            st.subheader("Predictions")

            if isinstance(predictions, tuple):
                detections = [predictions]
            else:
                detections = predictions

            for waste_type, confidence in detections:
                conf_val = float(confidence)
                conf_pct = conf_val * 100 if conf_val <= 1.0 else conf_val
                
                st.write(f"- **{waste_type.title()}** ({conf_pct:.1f}%)")
                add_detection(uploaded_file.name, waste_type, conf_val)

            st.success(f"Saved {len(detections)} detection(s) to History!")

elif page == "Detection History":

    st.header("Detection History")

    records = get_all_detections()

    if not records:
        st.info("No detection records found yet. Upload an image first!")
    else:
        st.caption(f"Showing {len(records)} record(s)")

        for record in records:
            det_id, image_name, waste_type, confidence, detected_at = parse_record(record)
            conf_pct = confidence * 100 if confidence <= 1.0 else confidence

            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                st.write(f"📄 **{image_name}**")
                st.caption(f"{waste_type.title()} — {conf_pct:.1f}% — {detected_at}")

            with col3:
                if st.button("Delete", key=f"delete_{det_id}"):
                    delete_detection(det_id)
                    st.rerun()

elif page == "Statistics":

    st.header("Statistics Dashboard")

    records = get_all_detections()

    if not records:
        st.info("No data yet. Upload and classify some images first!")
    else:
        parsed_records = [parse_record(r) for r in records]
        df = pd.DataFrame(
            parsed_records,
            columns=["id", "image_name", "waste_type", "confidence", "detected_at"]
        )

        df["confidence_pct"] = df["confidence"].apply(lambda x: x * 100 if x <= 1.0 else x)

        st.subheader("Totals")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Total Detections", len(df))
        with col_b:
            st.metric("Average Confidence", f"{df['confidence_pct'].mean():.1f}%")

        st.subheader("Counts per Category")
        category_counts = df["waste_type"].value_counts()
        st.bar_chart(category_counts)

        st.subheader("Category Distribution")
        fig, ax = plt.subplots()
        ax.pie(category_counts, labels=category_counts.index, autopct="%1.1f%%")
        st.pyplot(fig)

        st.subheader("Detections Over Time")
        df["date"] = df["detected_at"].astype(str).str[:10]
        daily_counts = df.groupby("date").size()
        st.line_chart(daily_counts)