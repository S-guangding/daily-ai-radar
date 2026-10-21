import requests
import json
from datetime import date
from collections import Counter

# --- Config ---
SOURCES = ['hackernews', 'github']  # easiy extendable
def fetch_hackernews():
    r = requests.get('https://hn.algolia.com/api/v1/search?query=AI&tags=story&numericFilters=created_at_i>' + str(int(__import__('time').time()) - 86400))
    return [item['title'] for item in r.json().get('hits', [])]

def fetch_github():
    r = requests.get('https://api.github.com/search/repositories?q=AI+created:>' + date.today().isoformat() + '&sort=stars&order=desc&per_page=10')
    return [item['full_name'] for item in r.json().get('items', [])]

# --- Aggregator ---
def gather():
    all_items = []
    for src in SOURCES:
        try:
            if src == 'hackernews':
                all_items.extend(fetch_hackernews())
            elif src == 'github':
                all_items.extend(fetch_github())
        except Exception as e:
            print(f'Error fetching {src}: {e}')
    return all_items

# --- Simple LLM-based summarizer (mock, replace with real call) ---
def summarize(items):
    # Mock of an LLM call; in reality you'd use an API like OpenAI
    # Here we just count keywords
    keywords = ['AI', 'model', 'LLM', 'agent', 'GPT', 'open source', 'training']
    found = [w for w in keywords if any(w.lower() in i.lower() for i in items)]
    return f"Today's AI radar: {len(items)} items. Hot topics: {', '.join(Counter(found).most_common(3)) if found else 'general AI'}"

# --- Main ---
def main():
    items = gather()
    if not items:
        summary = 'No AI news found today.'
    else:
        summary = summarize(items)
    # Output as simple digest
    print('=== Daily AI Radar ===')
    print(f'Date: {date.today()}')
    print(f'Total items: {len(items)}')
    print(f'Summary: {summary}')
    print('\nTop items:')
    for item in items[:5]:
        print(f'- {item}')

if __name__ == '__main__':
    main()
