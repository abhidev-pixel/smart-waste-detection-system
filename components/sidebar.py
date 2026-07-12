import streamlit as st

def show_sidebar():
    st.sidebar.title("Navigation")

    menu = st.sidebar.radio(
        "Menu",
        [
            "Dashboard",
            "Upload Image",
            "Detection History",
            "Statistics",
            "About"
        ]
    )

    return menu