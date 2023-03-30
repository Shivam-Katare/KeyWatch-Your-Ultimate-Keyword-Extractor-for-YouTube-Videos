import streamlit as st
from bs4 import BeautifulSoup
import requests
import re

st.markdown("<h1 style='text-align: center; text-decoration: underline'>KeyWatch</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Your Ultimate Keyword Extractor for YouTube Videos</h3>", unsafe_allow_html=True)
st.markdown("", unsafe_allow_html=True)

url = st.text_input("Enter YouTube video URL:")

if not url:
    st.warning("Please enter a YouTube video URL.")
else:
    # Extract video ID from URL
    video_id = None
    if "youtube.com" in url:
        match = re.search(r"v=([\w-]+)", url)
        if match:
            video_id = match.group(1)
    elif "youtu.be" in url:
        match = re.search(r"youtu.be/([\w-]+)", url)
        if match:
            video_id = match.group(1)

    if not video_id:
        st.warning("Please enter a valid YouTube video URL.")
    else:
        try:
            # Request and parse page
            full_url = f"https://www.youtube.com/watch?v={video_id}"
            page = requests.get(full_url)
            soup = BeautifulSoup(page.content, 'html.parser')

            # Extract keywords
            meta_tag = soup.select_one("meta[name=keywords]")
            if meta_tag:
                title = soup.find("title")
                keywords = meta_tag["content"].split(",")
                st.title("Title")
                st.markdown(f"<h4 style='color: #07ff89; font-family: Source Code Pro; background: black; border-radius: 9px; padding: 12px;'>{title.text}</h4>", unsafe_allow_html=True)
                st.title("Tags")
                st.markdown(f"<h5 style='background: white; color: black; font-family: math; padding: 14px; line-height: 30px; border: 2px solid; border-radius: 15px;font-weight: 700;'>{', '.join(keywords)}</h5>", unsafe_allow_html=True)
            else:
                st.warning("No keywords found.")
        except:
            st.error("An error occurred while trying to extract keywords. Please try again later.")
