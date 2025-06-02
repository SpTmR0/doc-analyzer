# AI-Powered Documentation Improvement Agent-1

A Python-based tool that scrapes articles from MoEngage URLs and analyzes their quality based on readability, structure, completeness, and style guidelines.

---

## Features

- **Web Scraping**: Uses Playwright to extract article content from MoEngage URLs
- **Readability Analysis**: Calculates Flesch Reading Ease and Gunning Fog Index scores
- **Structure Analysis**: Evaluates headings, paragraphs, lists, and links
- **Style Guide Compliance**: Checks against Microsoft Writing Style Guide principles
- **Grammar Check**: Identifies grammar and language issues using LanguageTool
- **Output Storage**: Saves both analysis reports (JSON) and extracted text (TXT)

---

## Installation

### 1. Clone the repository
```
git clone https://github.com/yourusername/doc-analyzer.git
cd doc-analyzer
```
### 2. Set up a virtual environment

```
python -m venv venv
venv\Scripts\activate       # On Windows
# or
source venv/bin/activate    # On macOS/Linux
```
### 3. Install required packages
```
pip install -r requirements.txt
```
### 4. Install Playwright browsers:
```
playwright install
```
### 5. Run the main script:
```
python main.py
```

## Output
- Console output shows extracted text and analysis report
- Files are saved in analysis_reports/ directory:
     - {domain}_{timestamp}.json - Complete analysis report
     - {domain}_{timestamp}.txt - Extracted article text

## Design Choices and Approach
- **Headless=False**: Required for MoEngage's Cloudflare protection
- **Readability Metrics**: Uses established algorithms (Flesch, Gunning Fog) for objective scoring
- **Structure Analysis**: Leverages HTML parsing to identify actual headings, lists, and links
- **Style Guide Implementation**:
   - Microsoft Writing Style Guide principles
   - Focus on clarity, conciseness, and user-centric language
   - Automated detection of passive voice, complex phrases, and formatting issues
- **Grammar Integration**: LanguageTool for comprehensive language checking

## Assumptions Made
- **Target Platform**: Designed specifically for MoEngage article URLs with article__body class structure
- **Content Language**: Assumes English content for grammar and readability analysis

## Challenges Faced 

### 1. Cloudflare Bot Protection
- Challenge: MoEngage uses Cloudflare which blocks automated scraping attempts.
- Solution:
  - Used headless=False to run visible browser
  - Added 8-second delay for bot check completion
  - Implemented slow_mo=100 for more human-like behavior
### 2. LLM Integration Limitations
- Challenge: Attempted to integrate advanced language models for more sophisticated content analysis.
- Issues Encountered:
  - OpenAI API: Requires paid subscription and API keys, making it inaccessible for free/open-source usage
  - Google Gemini: Also requires API keys and has usage costs
  - Open Source LLMs:
    - Local models (like distilbart-cnn) had insufficient performance for consistent content analysis
    - Inconsistent output formatting and reliability issues
    - High computational requirements for quality analysis
- Solution:
  - Implemented rule-based analysis using established libraries (textstat, language-tool-python)
  - Created custom Microsoft Style Guide compliance checker
  - Focused on objective, measurable metrics rather than subjective AI analysis
