import requests
from bs4 import BeautifulSoup
import json

def scrape_holidays():
    url = "https://www.calendarr.com/polska/kalendarz-swiat-nietypowych/"
    
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    holidays = []
    seen = set()  # Track unique holidays
    
    # Find all holiday entries
    for item in soup.find_all('div', class_='holiday-item'):
        try:
            # Extract data
            name_elem = item.find('h3')
            desc_elem = item.find('p')
            link_elem = item.find('a')
            date_elem = item.find('span', class_='date')
            
            if name_elem and desc_elem:
                name = name_elem.get_text(strip=True)
                description = desc_elem.get_text(strip=True)
                link = link_elem['href'] if link_elem else ""
                
                # Parse date
                if date_elem:
                    date_text = date_elem.get_text(strip=True)
                    # Parse day and month from date_text
                    # Format is usually "10 grudnia" or similar
                    parts = date_text.split()
                    if len(parts) >= 2:
                        day = int(parts[0])
                        month_name = parts[1].lower()
                        
                        # Polish month names to numbers
                        months = {
                            'stycznia': 1, 'lutego': 2, 'marca': 3, 'kwietnia': 4,
                            'maja': 5, 'czerwca': 6, 'lipca': 7, 'sierpnia': 8,
                            'września': 9, 'października': 10, 'listopada': 11, 'grudnia': 12
                        }
                        month = months.get(month_name, 1)
                        
                        # Create unique key
                        unique_key = (name, day, month)
                        
                        # Only add if not seen before
                        if unique_key not in seen:
                            seen.add(unique_key)
                            holidays.append({
                                'day': day,
                                'month': month,
                                'name': name,
                                'link': link,
                                'description': description
                            })
        except Exception as e:
            print(f"Error parsing item: {e}")
            continue
    
    return holidays

if __name__ == '__main__':
    print("Scraping holidays...")
    holidays = scrape_holidays()
    
    # Sort by month and day
    holidays.sort(key=lambda x: (x['month'], x['day']))
    
    # Save to JSON
    with open('nietypowe_swieta.json', 'w', encoding='utf-8') as f:
        json.dump(holidays, f, ensure_ascii=False, indent=2)
    
    print(f"Scraped {len(holidays)} unique holidays")
