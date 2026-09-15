import streamlit as st
from database.database import get_all_detections

def dashboard_cards():
    records = get_all_detections()
    total_scans = len(records)
    
    if total_scans > 0:
        confidences = [float(r.get("confidence", 0) if isinstance(r, dict) else r[3]) for r in records]
        confidences = [c * 100 if c <= 1.0 else c for c in confidences]
        avg_conf = sum(confidences) / total_scans
        
        categories = [r.get("waste_type") if isinstance(r, dict) else r[2] for r in records]
        top_cat = max(set(categories), key=categories.count).title()
    else:
        avg_conf = 0.0
        top_cat = "N/A"

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Scans</div>
                <div class="metric-value">{total_scans}</div>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Confidence</div>
                <div class="metric-value" style="color: #30D158;">{avg_conf:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Top Category</div>
                <div class="metric-value" style="color: #2997FF;">{top_cat}</div>
            </div>
        """, unsafe_allow_html=True)