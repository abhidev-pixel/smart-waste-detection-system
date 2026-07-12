import streamlit as st

def dashboard_cards():

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Images", "0")

    with col2:
        st.metric("Detections", "0")

    with col3:
        st.metric("Accuracy", "--")