# Kalbi Holidays 🎉

<!-- TODAY_HOLIDAYS_START -->
## 🎉 Today's Unusual Holidays (December 10, 2025)

### Human Rights Day

This holiday commemorates the signing of the Universal Declaration of Human Rights on December 10, 1948

[Learn more](https://www.kalbi.pl/dzien-praw-czlowieka)

---

### Bot Day

A bot is a program that performs specific activities instead of a human. Sometimes it makes our lives easier, but it's a delicate topic. What if bots will be able to help us with every activity, not only online?

[Learn more](https://www.kalbi.pl/dzien-bota)

---

### World Football Day

Of all the unimportant things, football is by far the most important. There is no point in arguing on a football day, you just have to go out and play with the boys.

[Learn more](https://www.kalbi.pl/swiatowy-dzien-futbolu)

---

<!-- TODAY_HOLIDAYS_END -->


A simple API that scrapes unusual/quirky holidays from the web and serves them as JSON. Perfect for Home Assistant integrations or just checking what weird celebration is happening today.

## What's this?

Ever wanted to know it's "International Talk Like a Pirate Day" or "National Pizza Day"? This scrapes those fun, unusual holidays and makes them available through a dead-simple JSON API.

The data updates automatically every day at 2 AM UTC, so you're always getting fresh info.

## Live API

The API is hosted on GitHub Pages:

**Polish:**
- **Today's holiday**: https://jeakob.github.io/kalbi-holidays/today.json
- **All holidays**: https://jeakob.github.io/kalbi-holidays/holidays.json

**English:**
- **Today's holiday**: https://jeakob.github.io/kalbi-holidays/today-english.json

**Docs**: https://jeakob.github.io/kalbi-holidays/

## Using with Home Assistant

If you want to display today's unusual holiday in Home Assistant, just add this to your `configuration.yaml`:

**Polish version:**
```yaml
sensor:
  - platform: rest
    name: Dzisiejsze Święto
    resource: https://jeakob.github.io/kalbi-holidays/today.json
    method: GET
    value_template: >
      {% if value_json[0].name is defined %}
        {{ value_json[0].name }}
      {% else %}
        Brak nietypowego święta
      {% endif %}
    json_attributes_path: $[0]
    json_attributes:
      - description
      - link
      - day
      - month
      - name
    scan_interval: 43200
```

**English version:**
```yaml
sensor:
  - platform: rest
    name: Today's Holiday
    resource: https://jeakob.github.io/kalbi-holidays/today-english.json
    method: GET
    value_template: >
      {% if value_json[0].name is defined %}
        {{ value_json[0].name }}
      {% else %}
        No unusual holiday today
      {% endif %}
    json_attributes_path: $[0]
    json_attributes:
      - description
      - link
      - day
      - month
      - name
    scan_interval: 43200
```

Then restart Home Assistant and you'll have a sensor that shows today's holiday.

## How it works

1. A GitHub Action runs daily (or when manually triggered)
2. The `kalbi.py` script scrapes holiday data from the web
3. Today's holiday gets auto-translated to English using Google Translate
4. The data gets saved as JSON files
5. Everything deploys to GitHub Pages automatically
6. You get a free, auto-updating API

Pretty straightforward.

## Data format

Each holiday looks like this:

```json
{
  "name": "Światowy Dzień Pizzy",
  "description": "Description of the holiday...",
  "link": "https://source-url.com",
  "day": 9,
  "month": 2
}
```

## Running locally

Want to run this yourself?

```bash
# Install dependencies
pip install requests beautifulsoup4

# Run the scraper
python kalbi.py

# You'll get a nietypowe_swieta.json file
```

## Credits

- Data scraped from [www.kalbi.pl](https://www.kalbi.pl/kalendarz-swiat-nietypowych))
- Original scraper concept from [piotrek77/kalbi](https://github.com/piotrek77/kalbi)

---

Questions? Issues? Feel free to open an issue or PR.
