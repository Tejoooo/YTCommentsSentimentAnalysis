import streamlit as st
import pandas as pd
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="yiour_api_key_here")

# Initialize the Chrome driver
def scrape_youtube_comments(url):
    # Set up Chrome options (optional)
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    
    service = Service(executable_path="./chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    items = []
    
    try:
        driver.get(url)

        # Initial scroll to trigger comments load
        time.sleep(3)
        driver.execute_script('window.scrollTo(0, 500);')
        time.sleep(3)

        # Scroll multiple times to load more comments (only 5 comments)
        for i in range(1):
            driver.execute_script('window.scrollBy(0, 3000);')
            time.sleep(3)

        # Extract usernames and comments (limit to 5 comments)
        username_elems = driver.find_elements(By.XPATH, '//*[@id="author-text"]')[:3]  # Limit to first 5
        comment_elems = driver.find_elements(By.XPATH, '//*[@id="content-text"]')[:3]  # Limit to first 5

        for username, comment in zip(username_elems, comment_elems):
            items.append({
                'Author': username.text.strip(),
                'Comment': comment.text.strip()
            })
        
        # Write to CSV
        filename = 'sample.csv'
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Author', 'Comment'])
            writer.writeheader()
            writer.writerows(items)

        print(f"✅ Extracted {len(items)} comments.")
    finally:
        driver.quit()
    
    return filename

# Function to classify comments using Gemini API
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

# Function to process the CSV and classify each comment
def process_comments():
    # Load the comments CSV
    df = pd.read_csv('sample.csv')
    
    # Classify comments using Gemini API
    df['Sentiment'] = df['Comment'].apply(lambda x: classify_comment_with_gemini(x))
    
    # Save to a new CSV
    df.to_csv('labeled_comments.csv', index=False, encoding='utf-8')
    
    return df

# Streamlit Interface
def main():
    st.title('YouTube Comment Scraper and Sentiment Analysis')

    st.subheader('Scrape YouTube Comments and Classify Them as Good or Bad')

    # Input for YouTube URL
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

        # Display the DataFrame
        st.subheader('Classified Comments')
        st.write(df)

        # Allow the user to download the CSV with classifications
        st.download_button(
            label="Download Classified Comments",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='labeled_comments.csv',
            mime='text/csv'
        )

# Run the app
if __name__ == '__main__':
    main()
