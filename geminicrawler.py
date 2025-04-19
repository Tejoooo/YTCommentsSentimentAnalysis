import streamlit as st
import pandas as pd
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import google.generativeai as genai

genai.configure(api_key="yiour_api_key_here")

def scrape_youtube_comments(url):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    
    service = Service(executable_path="./chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    items = []
    
    try:
        driver.get(url)
        time.sleep(3)
        driver.execute_script('window.scrollTo(0, 500);')
        time.sleep(3)
        for i in range(1):
            driver.execute_script('window.scrollBy(0, 3000);')
            time.sleep(3)

        username_elems = driver.find_elements(By.XPATH, '//*[@id="author-text"]')[:3]
        comment_elems = driver.find_elements(By.XPATH, '//*[@id="content-text"]')[:3]

        for username, comment in zip(username_elems, comment_elems):
            items.append({
                'Author': username.text.strip(),
                'Comment': comment.text.strip()
            })
        
        filename = 'sample.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Author', 'Comment'])
            writer.writeheader()
            writer.writerows(items)
        print(f"✅ Extracted {len(items)} comments.")
    finally:
        driver.quit()
    
    return filename

def classify_comment_with_gemini(comment):
    prompt = f"""The following is a YouTube comment in Telugu:
\"{comment}\"

Classify this comment as either "Good" (positive/neutral) or "Bad" (negative/abusive/offensive/harsh). 
Return only "Good" or "Bad" as your response."""
    
    try:
        response = genai.GenerativeModel('gemini-1.5-pro').generate_content(prompt)
        label = response.text.strip()
        return label
    except Exception as e:
        print(f"Error processing comment: {e}")
        return "Unknown"

def process_comments():
    df = pd.read_csv('sample.csv')
    df['Sentiment'] = df['Comment'].apply(lambda x: classify_comment_with_gemini(x))
    df.to_csv('labeled_comments.csv', index=False, encoding='utf-8')
    return df

def main():
    st.title('YouTube Comment Scraper and Sentiment Analysis')
    st.subheader('Scrape YouTube Comments and Classify Them as Good or Bad')
    youtube_url = st.text_input("Enter YouTube Video URL", "https://www.youtube.com/watch?v=IOopJ-PDpac")

    if st.button('Scrape Comments'):
        if youtube_url:
            st.text('Scraping YouTube comments...')
            filename = scrape_youtube_comments(youtube_url)
            st.success(f'Comments have been scraped and saved to {filename}')
        else:
            st.warning('Please enter a valid YouTube video URL.')

    if st.button('Classify Comments'):
        st.text('Classifying comments as Good or Bad...')
        df = process_comments()
        st.success('Classification completed!')
        st.subheader('Classified Comments')
        st.write(df)
        st.download_button(
            label="Download Classified Comments",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='labeled_comments.csv',
            mime='text/csv'
        )

if __name__ == '__main__':
    main()
