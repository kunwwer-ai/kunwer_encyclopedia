import streamlit as st
from streamlit_option_menu import option_menu

def apply_dashboard_layout():
    st.set_page_config(page_title="Kunwer Sachdev Encyclopedia", layout="wide")

    st.markdown("""
        <style>
            .block-container {padding-top: 2rem;}
            .metric-box {
                border-radius: 10px;
                background-color: white;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                text-align: center;
            }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        selected = option_menu(
            "Encyclopedia",
            [
                "Overview", "Biography", "YouTube", "Articles",
                "Books", "News", "Social Media",
                "Real-Time Scraper" , "Web"  # ✅ Added new tab
            ],
            icons=[
                "bar-chart-line", "person", "youtube", "file-earmark-text",
                "book", "newspaper", "globe",
                "bolt"  # ⚡ Icon for real-time scraper
            ],
            menu_icon="book",
            default_index=0,
            styles={
                "container": {"background-color": "#fff"},
                "icon": {"color": "#2e86de", "font-size": "18px"},
                "nav-link": {"font-size": "16px", "--hover-color": "#f0f0f0"},
                "nav-link-selected": {"background-color": "#e6f0fa"},
            }
        )
    return selected
