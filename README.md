# Whatsap-Chat-Analyzer-
A Python-based tool to analyze WhatsApp chat exports and generate insights like message counts, word frequencies, most active users, and more.

🔧 Features
Total messages, words, media shared, and links

Most active participants

Daily and monthly message trends

Emoji usage analysis

Word cloud generation

Language detection (optional)

Sentiment analysis (optional)

📁 Input
Export your WhatsApp chat as a .txt file (without media) and upload it.

📦 Requirements
Python 3.7+

pandas

matplotlib

seaborn

wordcloud

emoji

regex

Optional: nltk, langdetect, textblob for NLP features

Install dependencies with:

bash
Copy
Edit
pip install -r requirements.txt
▶️ Usage
bash
Copy
Edit
python main.py chat.txt
Or run it as a Streamlit app:

bash
Copy
Edit
streamlit run app.py
📈 Sample Output
Message frequency graph

Top words cloud

Emoji pie chart

User contribution bar chart

🛠️ How it Works
Parses the .txt file line-by-line

Extracts sender, timestamp, and message content

Applies NLP/statistics to generate insights

Outputs visuals and summaries

📝 To-Do
Group chat vs individual chat distinction

Support for different locales (date formats)

Export results as PDF/CSV
