!pip install newspaper3k GoogleNews transformers sentence-transformers faiss-cpu -q

import newspaper
from GoogleNews import GoogleNews 
from transformers import pipeline
import nltk

# NLTK is required for article parsing
nltk.download('punkt')

try:
    analyst
except NameError:
    print("Initializing system...")
    analyst = pipeline("summarization", model="facebook/bart-large-cnn", device_map="auto")

def fetch_article_context(ticker):
    print(f"Scanning deep-web sources for: {ticker}...")
    
    googlenews = GoogleNews(period='2d')
    googlenews.search(f"{ticker} stock analysis")
    results = googlenews.result()
    
    gathered_intel = []
    scan_limit = 3 
    scanned_count = 0
    
    for item in results:
        if scanned_count >= scan_limit:
            break
            
        try:
            article = newspaper.Article(item['link'])
            article.download()
            article.parse()
            
            # Filter out empty or login-walled articles
            if len(article.text) > 500:
                # Truncate to first 1200 chars to maintain focus
                gathered_intel.append(article.text[:1200])
                scanned_count += 1
        except:
            continue
            
    if not gathered_intel:
        return ""
        
    return " ".join(gathered_intel)

def generate_market_report(ticker):
    raw_data = fetch_article_context(ticker)
    
    if len(raw_data) < 200:
        return "Insufficient accessible data for deep analysis."
        
    # Summarize the combined text into a single insight
    # Min_length ensures it doesn't just output a single sentence
    report = analyst(
        raw_data[:3500], 
        max_length=200, 
        min_length=80, 
        do_sample=False
    )
    
    return report[0]['summary_text']

# Main Execution Block
if __name__ == "__main__":
    target_ticker = "AAPL"
    print(f"\nRequesting Deep Analysis for: {target_ticker}")
    
    insight = generate_market_report(target_ticker)
    
    print("\n--- ANALYST REPORT ---")
    print(insight)
