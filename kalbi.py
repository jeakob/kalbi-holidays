import requests
from bs4 import BeautifulSoup
import json

def scrape_holidays():
    """Scrape holidays from kalbi.pl"""
    
    holidays = []
    seen = set()  # Track unique holidays
    
    # Month names in Polish
    months_pl = [
        'styczen', 'luty', 'marzec', 'kwiecien', 'maj', 'czerwiec',
        'lipiec', 'sierpien', 'wrzesien', 'pazdziernik', 'listopad', 'grudzien'
    ]
    
    # Scrape each month's page
    for month_num, month_name in enumerate(months_pl, 1):
        url = f"https://www.kalbi.pl/kalendarz-swiat-nietypowych-{month_name}"
        
        try:
            print(f"Scraping {month_name}...")
            response = requests.get(url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all holiday items - adjust selectors based on actual HTML structure
            # This is a generic approach that should work with most structures
            holiday_items = soup.find_all(['article', 'div'], class_=lambda x: x and ('holiday' in x.lower() or 'day' in x.lower() or 'event' in x.lower()))
            
            for item in holiday_items:
                try:
                    # Try to find title/name
                    title = item.find(['h2', 'h3', 'h4', 'a'])
                    if not title:
                        continue
                    
                    name = title.get_text(strip=True)
                    
                    # Skip if empty or too short
                    if not name or len(name) < 3:
                        continue
                    
                    # Try to find description
                    desc_elem = item.find('p')
                    description = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    # Try to find link
                    link_elem = item.find('a', href=True)
                    link = f"https://www.kalbi.pl{link_elem['href']}" if link_elem and link_elem['href'].startswith('/') else (link_elem['href'] if link_elem else "")
                    
                    # Try to extract day from various possible formats
                    day = None
                    day_elem = item.find(text=lambda t: t and any(char.isdigit() for char in str(t)))
                    if day_elem:
                        import re
                        numbers = re.findall(r'\d+', str(day_elem))
                        if numbers:
                            day = int(numbers[0])
                            # Validate day is reasonable (1-31)
                            if day < 1 or day > 31:
                                day = None
                    
                    # If we couldn't extract day, skip this item
                    if not day:
                        continue
                    
                    # Create unique key
                    unique_key = (name, day, month_num)
                    
                    # Only add if not seen before
                    if unique_key not in seen:
                        seen.add(unique_key)
                        holidays.append({
                            'day': day,
                            'month': month_num,
                            'name': name,
                            'link': link,
                            'description': description
                        })
                
                except Exception as e:
                    print(f"Error parsing item: {e}")
                    continue
            
        except Exception as e:
            print(f"Error scraping {month_name}: {e}")
            continue
    
    return holidays

if __name__ == '__main__':
    print("Scraping holidays from kalbi.pl...")
    holidays = scrape_holidays()
    
    # Sort by month and day
    holidays.sort(key=lambda x: (x['month'], x['day']))
    
    # Save to JSON
    with open('nietypowe_swieta.json', 'w', encoding='utf-8') as f:
        json.dump(holidays, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Scraped {len(holidays)} unique holidays")
    print(f"Saved to nietypowe_swieta.json")
