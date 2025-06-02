from transformers import pipeline

# Load a pre-trained summarization model (lightweight, free-tier compatible)
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def get_llm_suggestions(text):
    short_text = text[:1000]      #max limit is 1024 tokens(1000 characters)                
    summary = summarizer(short_text)[0]['summary_text']  #generating summary/suggestions

    return {
        "summary_of_issues": summary,
    }
