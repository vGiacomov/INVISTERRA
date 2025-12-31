import streamlit as st
from Pages import home, indeksy, maps
from Pages.Themes import apply_theme, hide_sidebar, show_sidebar

st.set_page_config(
    page_title="INVISTERRA",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_theme()

#st.markdown("<hr style='margin: 0rem 0 0rem 0; border: 0; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏠 HOME", "📊 INDEKSY", "🗺️ MAPS"])

with tab1:
    hide_sidebar()
    home.render()

with tab2:
    hide_sidebar()
    indeksy.render()

with tab3:
    show_sidebar()
    maps.render()

st.markdown("""
<div class="custom-footer">
    JAKUB MIELCAREK 2025
</div>
""", unsafe_allow_html=True)
