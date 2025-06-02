from webscrap import fetch_article_text        
from analyzer import analyze_document          
import json
import os
from datetime import datetime
from urllib.parse import urlparse

url = input("Enter MoEngage article URL: ")    #user input
try:
    article_text, html_content = fetch_article_text(url)
    report = analyze_document(url, article_text, html_content)
    print(json.dumps(report, indent=2))
    
    output_dir = "analysis_reports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    #generating filename from URL and timestamp
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace("www.", "")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_filename = f"{domain}_{timestamp}"
    
    #save report to JSON file
    json_filepath = os.path.join(output_dir, f"{base_filename}.json")
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    #saving extracted text to .TXT 
    txt_filepath = os.path.join(output_dir, f"{base_filename}.txt")
    with open(txt_filepath, 'w', encoding='utf-8') as f:
        f.write(f"URL: {url}\n")
        f.write(f"Extracted on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        f.write(article_text)
    
    print(f"\nFiles saved:")
    print(f"  Analysis report: {json_filepath}")
    print(f"  Extracted text: {txt_filepath}")
    
except Exception as e:
    print(f"An error occurred: {e}")