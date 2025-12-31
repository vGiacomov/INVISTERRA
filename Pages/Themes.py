import streamlit as st


def apply_theme() -> None:
    """Single, always-light theme + all app CSS."""
    st.markdown("""
    <style>
        /* Import Google Fonts - Figtree (ciepła, przyjazna) */
        @import url('https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;600;700&display=swap');

        /* =========================
           GLOBAL: wymuś jasny wygląd + czcionka Figtree
           ========================= */

        /* Root aplikacji */
        div[data-testid="stAppViewContainer"] {
            background-color: #ffffff !important;
            color: #000000 !important;
            font-family: 'Figtree', sans-serif !important;
        }

        /* Główna sekcja */
        div[data-testid="stAppViewContainer"] section.main {
            background-color: #ffffff !important;
        }

        /* Kontener z treścią */
        .main .block-container {
            max-width: 100%;
            padding-left: 2rem;
            padding-right: 2rem;
            padding-top: 1rem;
            padding-bottom: 4rem;
            background-color: #ffffff !important;
            color: #000000 !important;
            font-family: 'Figtree', sans-serif !important;
        }

        /* Wymuszenie czarnej czcionki na wszystkich elementach */
        *, p, span, div, label, h1, h2, h3, h4, h5, h6 {
            color: #000000 !important;
            font-family: 'Figtree', sans-serif !important;
        }

        /* =========================
           SIDEBAR: jasny styl
           ========================= */

        section[data-testid="stSidebar"] {
            background-color: #f8f9fa !important;
            border-right: 1px solid #ddd !important;
        }

        section[data-testid="stSidebar"] > div {
            background-color: #f8f9fa !important;
            padding-top: 2rem !important;
        }

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {
            color: #000000 !important;
        }

        /* File uploader */
        section[data-testid="stSidebar"] div[data-testid="stFileUploader"] {
            background-color: #ffffff !important;
            border: 2px dashed #ddd !important;
            border-radius: 8px !important;
            padding: 1rem !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stFileUploader"] > div {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stFileUploader"] section {
            background-color: #ffffff !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stFileUploader"] small {
            color: #666666 !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stFileUploader"] label {
            color: #000000 !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stFileUploadDropzone"] {
            background-color: #ffffff !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stFileUploadDropzone"] > div {
            background-color: #ffffff !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stFileUploadDropzone"] span {
            color: #000000 !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stFileUploader"] button {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #ddd !important;
        }

        /* Selectbox */
        section[data-testid="stSidebar"] div[data-baseweb="select"] {
            background-color: #ffffff !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #ddd !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] div[role="button"] {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] input {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] svg {
            fill: #000000 !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="select"] span {
            color: #000000 !important;
        }

        /* Dropdown menu */
        div[data-baseweb="popover"] {
            background-color: #ffffff !important;
        }

        ul[role="listbox"] {
            background-color: #ffffff !important;
        }

        ul[role="listbox"] li {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        ul[role="listbox"] li:hover {
            background-color: #f0f0f0 !important;
        }

        /* Input fields */
        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] textarea {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #ddd !important;
        }

        /* Przyciski w sidebar */
        section[data-testid="stSidebar"] button {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #ddd !important;
        }

        section[data-testid="stSidebar"] button:hover {
            background-color: #f0f0f0 !important;
            border-color: #bbb !important;
        }

        /* Primary button (🚀 Run Analysis) */
        section[data-testid="stSidebar"] button[kind="primary"],
        section[data-testid="stSidebar"] button[data-testid="baseButton-primary"] {
            background-color: #ffffff !important;
            color: #FF4B4B !important;
            border: 2px solid #FF4B4B !important;
            font-weight: 600 !important;
        }

        section[data-testid="stSidebar"] button[kind="primary"]:hover,
        section[data-testid="stSidebar"] button[data-testid="baseButton-primary"]:hover {
            background-color: #FF4B4B !important;
            color: #ffffff !important;
            border: 2px solid #FF4B4B !important;
        }

        /* Checkboxy */
        section[data-testid="stSidebar"] input[type="checkbox"] {
            accent-color: #FF4B4B !important;
        }

        /* =========================
           HOME: powiększone i wyrównane do prawej
           ========================= */

        .welcome-container {
            text-align: right !important;
            padding-right: 2rem;
        }

        .welcome-title {
            font-size: 7.5rem !important;
            font-weight: 700 !important;
            margin-top: 16rem !important;
            margin-bottom: 0.2rem !important;
            color: #000000 !important;
            line-height: 1.2 !important;
            font-family: 'Figtree', sans-serif !important;
        }

        .welcome-subtitle {
            font-size: 3rem !important;
            font-weight: 400 !important;
            color: #000000 !important;
            font-style: italic;
            line-height: 1.4 !important;
            font-family: 'Figtree', sans-serif !important;
        }

        /* =========================
           PRZYCISKI W MAIN CONTENT - BARDZO AGRESYWNE REGUŁY
           ========================= */

        /* WSZYSTKIE przyciski poza sidebarem */
        .stButton button,
        .stButton > button,
        div[data-testid="column"] button,
        .main button,
        button[kind="secondary"],
        button[data-testid="baseButton-secondary"] {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #000000 !important;
            border-radius: 10px !important;
            padding: 1rem 2.5rem !important;
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            font-family: 'Figtree', sans-serif !important;
            transition: all 0.3s ease !important;
            cursor: pointer !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }

        .stButton button:hover,
        .stButton > button:hover,
        div[data-testid="column"] button:hover,
        .main button:hover,
        button[kind="secondary"]:hover,
        button[data-testid="baseButton-secondary"]:hover {
            background-color: #000000 !important;
            color: #ffffff !important;
            border: 2px solid #000000 !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        }

        /* Konkretnie dla przycisku z key="start_btn" */
        button[data-testid="baseButton-secondary"][key="start_btn"] {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 2px solid #000000 !important;
        }

        /* =========================
           UKRYWANIE: elementy Streamlit
           ========================= */

        #MainMenu { visibility: hidden; }
        header { visibility: hidden; }
        footer { visibility: hidden; }

        div[data-testid="stSidebarNav"] { display: none !important; }

        [data-testid="stSidebar"] { display: none; }
        section[data-testid="stSidebar"] { display: none; }

        /* =========================
           TABS: wygląd zakładek
           ========================= */

        .stTabs { margin-top: 0; }

        .stTabs [data-baseweb="tab-list"] {
            gap: 2rem;
            justify-content: center;
            background-color: transparent;
            border-bottom: 2px solid #ddd;
            padding-bottom: 0;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 0.8rem 2rem;
            font-size: 1.1rem;
            font-weight: 600;
            background-color: transparent;
            border: none;
            color: #000000 !important;
            font-family: 'Figtree', sans-serif !important;
        }

        .stTabs [aria-selected="true"] {
            border-bottom: 3px solid #FF4B4B;
            background-color: transparent;
            color: #000000 !important;
        }

        /* =========================
           STOPKA
           ========================= */

        .custom-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f0f0f0;
            color: #000000 !important;
            text-align: center;
            padding: 0.8rem;
            font-size: 0.95rem;
            font-weight: 600;
            border-top: 1px solid #ddd;
            z-index: 999;
            font-family: 'Figtree', sans-serif !important;
        }
    </style>
    """, unsafe_allow_html=True)


def show_sidebar() -> None:
    """Pokaż sidebar (tylko dla MAPS)."""
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: block !important; }
        section[data-testid="stSidebar"] { display: block !important; }
    </style>
    """, unsafe_allow_html=True)


def hide_sidebar() -> None:
    """Ukryj sidebar (dla HOME i INDEKSY)."""
    st.markdown("""
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        section[data-testid="stSidebar"] { display: none !important; }
    </style>
    """, unsafe_allow_html=True)
