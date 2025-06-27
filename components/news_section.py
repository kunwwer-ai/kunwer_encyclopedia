# components/news_section.py

import streamlit as st

def show_news_section(news_data):
    st.markdown("### 🗞️ <span style='color:#2e86de;'>News Highlights</span>", unsafe_allow_html=True)

    if news_data:
        for item in news_data:
            with st.expander(item.get("title", "📰 Untitled News")):
                st.write(f"**📅 Date:** {item.get('date', 'Unknown')}")
                st.write(f"**📰 Source:** {item.get('source', 'Unknown')}")
                st.write(f"**🧾 Snippet:** {item.get('snippet', 'No summary available.')}")

                content = item.get("content")
                if content:
                    st.markdown("**📰 Full Article Content:**")
                    st.markdown(content)

                if item.get("link"):
                    st.markdown(f"[🔗 Read Full Article]({item['link']})")
                else:
                    st.info("🔍 No link available.")
    else:
        st.info("No news articles found.")
