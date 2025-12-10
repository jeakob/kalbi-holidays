name: Scrape and Publish Holidays

on:
  schedule:
    - cron: '0 2 * * *'
  workflow_dispatch:
  push:
    branches:
      - main

permissions:
  contents: write
  pages: write
  id-token: write

jobs:
  scrape-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install requests beautifulsoup4 deep-translator
      
      - name: Run scraper
        run: python kalbi.py
      
      - name: Create public directory
        run: mkdir -p public
      
      - name: Copy holidays JSON
        run: cp nietypowe_swieta.json public/holidays.json
      
      - name: Create today endpoint
        run: |
          python3 -c "
          import json
          from datetime import datetime
          
          with open('nietypowe_swieta.json', 'r', encoding='utf-8') as f:
              data = json.load(f)
          
          now = datetime.now()
          today = [h for h in data if h['day'] == now.day and h['month'] == now.month]
          
          with open('public/today.json', 'w', encoding='utf-8') as f:
              json.dump(today, f, ensure_ascii=False, indent=2)
          "
      
      - name: Translate to English
        run: |
          python3 -c "
          import json
          from deep_translator import GoogleTranslator
          from datetime import datetime
          
          translator = GoogleTranslator(source='pl', target='en')
          
          # Load Polish data
          with open('nietypowe_swieta.json', 'r', encoding='utf-8') as f:
              data = json.load(f)
          
          # Get today's holiday
          now = datetime.now()
          today = [h for h in data if h['day'] == now.day and h['month'] == now.month]
          
          # Translate only today's holiday
          today_en = []
          for holiday in today:
              try:
                  translated = {
                      'name': translator.translate(holiday['name']),
                      'description': translator.translate(holiday['description']),
                      'link': holiday['link'],
                      'day': holiday['day'],
                      'month': holiday['month']
                  }
                  today_en.append(translated)
              except Exception as e:
                  print(f'Error translating: {e}')
                  today_en.append(holiday)  # Keep original if translation fails
          
          # Save today-english.json
          with open('public/today-english.json', 'w', encoding='utf-8') as f:
              json.dump(today_en, f, ensure_ascii=False, indent=2)
          "

      
      - name: Create HTML page
        run: |
          cat > public/index.html <<'EOF'
          <!DOCTYPE html>
          <html>
          <head>
              <meta charset="UTF-8">
              <title>Kalbi Holidays API</title>
          </head>
          <body>
              <h1>Kalbi Holidays API</h1>
              <p>Endpoints:</p>
              <h3>Polish (Polski)</h3>
              <ul>
                  <li><a href="today.json">today.json</a> - Dzisiejsze swiento</li>
                  <li><a href="holidays.json">holidays.json</a> - Wszystkie swienta</li>
              </ul>
              <h3>English</h3>
              <ul>
                  <li><a href="today-english.json">today-english.json</a> - Today's holiday</li>
              </ul>
              <h2>Home Assistant Config</h2>
              <h3>Polish Version</h3>
              <pre>
          sensor:
            - platform: rest
              name: Dzisiejsze Swiento
              resource: https://jeakob.github.io/kalbi-holidays/today.json
              method: GET
              scan_interval: 43200
              </pre>
              <h3>English Version</h3>
              <pre>
          sensor:
            - platform: rest
              name: Today's Holiday
              resource: https://jeakob.github.io/kalbi-holidays/today-english.json
              method: GET
              scan_interval: 43200
              </pre>
          </body>
          </html>
          EOF
      
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: 'public'
      
      - name: Deploy to GitHub Pages
        uses: actions/deploy-pages@v4
