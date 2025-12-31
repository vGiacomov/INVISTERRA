import streamlit as st
from PIL import Image
import streamlit.components.v1 as components


def render():
    col1, col2 = st.columns([1, 2])

    with col1:
        # Load and display logo - LEFT ALIGNED
        try:
            logo = Image.open("logo/logo.png")
            st.image(logo)
        except FileNotFoundError:
            st.markdown("""
            <div class="logo-container">
                <div style="text-align: center; width: 150%;">
                    <h2>🛰️</h2>
                    <p style="font-size: 0.8rem; opacity: 0.6;">Place your logo.png file here</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        # Welcome section - RIGHT ALIGNED
        st.markdown("""
        <div class="welcome-container">
            <h1 class="welcome-title">WELCOME IN INVISTERRA</h1>
            <p class="welcome-subtitle">Seeing beyond the visible</p>
        </div>
        """, unsafe_allow_html=True)

        # Let's start button - right aligned
        col_spacer, col_btn = st.columns([1, 1])
        with col_btn:
            if st.button("LET'S START", use_container_width=True, key="start_btn"):
                components.html(
                    """
                    <script>
                    window.parent.document.querySelectorAll('button[data-baseweb="tab"]')[2].click();
                    </script>
                    """,
                    height=0,
                )
