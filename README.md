# 🎥 YouTube Comment Scraper & Sentiment Classifier

This Streamlit-based tool allows you to:

✅ Scrape **YouTube comments** from a video  
✅ Classify comments as **Good** or **Bad** using **Gemini AI** (Google's Gemini 1.5 Pro)  
✅ Export labeled comments to a CSV

---

## 🚀 Features

- Extracts the **top 3 comments** from a YouTube video using **Selenium**
- Classifies comments with Google Gemini as either:
  - `Good` (positive/neutral)
  - `Bad` (offensive/abusive/negative)
- Displays the results in a **Streamlit dashboard**
- Allows downloading the final labeled comments as a CSV

---

## 🛠 Requirements

- Python 3.7+
- [Google Gemini API key](https://makersuite.google.com/app)
- Chrome browser & matching [ChromeDriver](https://chromedriver.chromium.org/downloads)

### 🔧 Install dependencies

```bash
pip install streamlit selenium pandas google-generativeai
```

### 📦 Folder structure

```
.
├── app.py                   # Main Streamlit app
├── chromedriver.exe         # Required by Selenium (download separately)
├── sample.csv               # Temp scraped comments
├── labeled_comments.csv     # Output with sentiment
└── README.md
```

---

## 🔑 Setup

1. Replace the line below in `app.py` with your actual Gemini API key:

```python
genai.configure(api_key="your_api_key_here")
```

2. Ensure you have the correct `chromedriver.exe` matching your Chrome version and placed in the project root.

3. Run the app:

```bash
streamlit run app.py
```

---

## 📸 Example

You can visualize a dashboard like this:

```
+----------------+------------------------------+-----------+
| Author         | Comment                      | Sentiment |
+----------------+------------------------------+-----------+
| John Doe       | This video is amazing!       | Good      |
| Jane Smith     | Waste of time. Don’t watch.  | Bad       |
+----------------+------------------------------+-----------+
```

---

## 🤖 AI Classification Logic

Each comment is sent to Gemini with the following prompt:

> Classify this comment as either "Good" (positive/neutral) or "Bad" (negative/abusive/offensive/harsh). Return only "Good" or "Bad".

---

## 📥 Output

After classification, a file `labeled_comments.csv` is created with:

| Author     | Comment                            | Sentiment |
|------------|-------------------------------------|-----------|
| John Doe   | This video is amazing!              | Good      |
| Jane Smith | Waste of time. Don’t watch it.      | Bad       |

---

## 🛡️ Disclaimer

This tool scrapes YouTube via automation, which may violate their terms of service. Use responsibly and for educational purposes.

---

## 🙌 Acknowledgments

- [Streamlit](https://streamlit.io/)
- [Google Generative AI (Gemini)](https://ai.google.dev/)
- [Selenium](https://www.selenium.dev/)

---

## 📄 License

MIT License