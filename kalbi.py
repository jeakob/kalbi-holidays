import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_holidays():
    holidays = []
    seen = set()
    
    months_pl = [
        'styczen', 'luty', 'marzec', 'kwiecien', 'maj', 'czerwiec',
        'lipiec', 'sierpien', 'wrzesien', 'pazdziernik', 'listopad', 'grudzien'
    ]
    
    for month_num, month_name in enumerate(months_pl, 1):
        url = f"https://www.kalbi.pl/kalendarz-swiat-nietypowych-{month_name}"
        
        try:
            print(f"Scraping {month_name}...")
            response = requests.get(url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            day_items = soup.find_all('li')
            
            for item in day_items:
                try:
                    day_link = item.find('a', href=re.compile(r'/\d+-'))
                    if not day_link:
                        continue
                    
                    day_text = day_link.get_text()
                    day_match = re.search(r'(\d+)', day_text)
                    if not day_match:
                        href = day_link.get('href', '')
                        day_match = re.search(r'/(\d+)-', href)
                    
                    if not day_match:
                        continue
                    
                    day = int(day_match.group(1))
                    
                    holiday_headers = item.find_all('h3')
                    
                    for h3 in holiday_headers:
                        holiday_link = h3.find('a')
                        if not holiday_link:
                            continue
                        
                        name = holiday_link.get_text(strip=True)
                        
                        if not name or len(name) < 3:
                            continue
                        
                        if any(month in name.lower() for month in months_pl):
                            continue
                        if re.match(r'^\d+$', name):
                            continue
                        
                        href = holiday_link.get('href', '')
                        if href and not href.startswith('http'):
                            link = f"https://www.kalbi.pl{href}"
                        else:
                            link = href
                        
                        description = ""
                        current = h3
                        while current:
                            current = current.next_sibling
                            if current is None:
                                break
                            
                            if isinstance(current, str):
                                text = current.strip()
                                if text and len(text) > 20:
                                    description = text
                                    break
                            elif hasattr(current, 'name') and current.name == 'h3':
                                break
                            elif hasattr(current, 'get_text'):
                                text = current.get_text(strip=True)
                                if text and len(text) > 20:
                                    description = text
                                    break
                        
                        unique_key = (name, day, month_num)
                        
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
            
            count = len([h for h in holidays if h['month'] == month_num])
            print(f"  Found {count} holidays")
            
        except Exception as e:
            print(f"Error scraping {month_name}: {e}")
            continue
    
    return holidays

if __name__ == '__main__':
    print("Scraping holidays from kalbi.pl...")
    holidays = scrape_holidays()
    
    holidays.sort(key=lambda x: (x['month'], x['day']))
    
    with open('nietypowe_swieta.json', 'w', encoding='utf-8') as f:
        json.dump(holidays, f, ensure_ascii=False, indent=2)
    
    print(f"\nScraped {len(holidays)} unique holidays")
    print("Saved to nietypowe_swieta.json")
