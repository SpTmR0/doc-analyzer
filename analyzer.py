import textstat
import language_tool_python
from bs4 import BeautifulSoup

tool = language_tool_python.LanguageTool('en-US')

def check_style_guide_microsoft(text):
    issues = []

    #Passive voice phrases
    passive_phrases = ['is being', 'was done', 'has been', 'will be', 'are being', 'were made']
    for phrase in passive_phrases:
        if phrase in text:
            issues.append(f"Possible passive voice usage: '{phrase}'")

    #Complex/wordy phrases
    complex_words = {
        'utilize': 'use',
        'prior to': 'before',
        'in order to': 'to',
        'terminate': 'end',
        'commence': 'begin',
        'assist': 'help',
        'endeavor': 'try'
    }
    for word, suggestion in complex_words.items():
        if word in text.lower():
            issues.append(f"Use simpler alternative for '{word}' → '{suggestion}'")

    #Use of "the user" instead of "you"
    if 'the user' in text.lower():
        issues.append("Consider using 'you' instead of 'the user'.")

    #Sentence-style capitalization issues
    lines = text.splitlines()
    for line in lines:
        words = line.strip().split()
        if len(words) >= 2 and all(w[0].isupper() for w in words[:3]):
            issues.append(f"Possible title-case used instead of sentence case: '{line.strip()}'")

    #Avoid exclamation marks
    if "!" in text:
        issues.append("Avoid exclamation marks in formal writing.")

    return issues


def analyze_document(url, article_text, html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    text = article_text

    #Readability
    flesch_score = textstat.flesch_reading_ease(text)
    gunning_fog = textstat.gunning_fog(text)

    readability_feedback = []
    if flesch_score < 60:
        readability_feedback.append("Flesch score suggests content may be complex.")
    if gunning_fog > 12:
        readability_feedback.append(f"Gunning Fog Index = {gunning_fog:.2f}, which means it's suitable for college-level readers.")
    if not readability_feedback:
        readability_feedback = ["Content is readable for a general marketing audience."]

    #structure Analysis
    headings = soup.find_all(['h1', 'h2', 'h3'])
    long_paragraphs = [p for p in text.split('\n') if len(p.split()) > 50]
    lists = soup.find_all(['ul', 'ol'])
    links = soup.find_all('a')

    heading_levels = [int(tag.name[1]) for tag in headings if tag.name[1].isdigit()]
    skipped_headings = any(
        abs(curr - prev) > 1 for prev, curr in zip(heading_levels, heading_levels[1:])
    )

    structure_suggestions = []
    if long_paragraphs:
        structure_suggestions.append("Split long paragraphs for better readability.")
    if len(headings) < 3:
        structure_suggestions.append("Add more subheadings to improve scannability.")
    if len(lists) < 1:
        structure_suggestions.append("Use numbered or bulleted lists to explain steps clearly.")
    if len(links) < 2:
        structure_suggestions.append("Include links to related documentation or FAQs.")
    if skipped_headings:
        structure_suggestions.append("Avoid skipping heading levels (e.g., h1 to h3 directly).")

    #Completeness Check
    has_examples = any(kw in text.lower() for kw in ["for example", "e.g.", "example", "code snippet"])
    completeness_feedback = "Sufficient examples present." if has_examples else "Add examples for better understanding."

    #Style/Grammar Check
    grammar_issues = tool.check(text)
    grammar_suggestions = [{
        "message": issue.message,
        "suggestion": issue.replacements,
        "context": issue.context.strip()
    } for issue in grammar_issues[:5]]

    microsoft_style_issues = check_style_guide_microsoft(text)

    #Final Report
    return {
        "url": url,
        "readability": {
            "flesch_reading_ease": flesch_score,
            "gunning_fog_index": gunning_fog,
            "feedback": readability_feedback
        },
        "structure": {
            "heading_count": len(headings),
            "long_paragraphs": len(long_paragraphs),
            "list_count": len(lists),
            "link_count": len(links),
            "skipped_heading_levels": skipped_headings,
            "suggestions": structure_suggestions
        },
        "completeness": {
            "has_examples": has_examples,
            "feedback": completeness_feedback
        },
        "style_guide": {
            "grammar_issues_found": len(grammar_issues),
            "sample_issues": grammar_suggestions,
            "microsoft_style_guide_violations": microsoft_style_issues
        }
    }
