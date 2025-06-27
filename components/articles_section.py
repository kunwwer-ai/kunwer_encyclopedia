import streamlit as st

def show_articles_section(articles_data):
    st.header("📰 Articles & Web Presence")

    if not articles_data:
        st.info("⚠️ No article data loaded.")
        return

    for article in articles_data:
        title = article.get("title", "Untitled Article")
        link = article.get("link", "N/A")
        snippet = article.get("snippet", "No snippet available.")
        content = article.get("content", "")
        source = article.get("source", "Web")
        date = article.get("date", "N/A")

        with st.expander(f"🔗 {title}"):
            st.markdown(f"<h3 style='color:#2e86de; margin-top:0;'>{title}</h3>", unsafe_allow_html=True)
            st.markdown(f"**🗞️ Source:** {source} &nbsp;&nbsp;|&nbsp;&nbsp; 📅 **Date:** {date}", unsafe_allow_html=True)
            st.markdown(f"🔗 [Read Full Article]({link})", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown(f"📄 **Snippet Preview:** {snippet}")

            if content:
                with st.expander("📖 Show Full Extracted Text"):
                    st.markdown(content)