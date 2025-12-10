import requests
from bs4 import BeautifulSoup
import json

# Mapa miesięcy po polsku
months = {
    'styczeń': 1, 'luty': 2, 'marzec': 3, 'kwiecień': 4,
    'maj': 5, 'czerwiec': 6, 'lipiec': 7, 'sierpień': 8,
    'wrzesień': 9, 'październik': 10, 'listopad': 11, 'grudzień': 12
}

# Lista na dane
holidays = []

# Iteracja po wszystkich miesiącach (od stycznia do grudnia)
for month_name, month_num in months.items():
    # Generowanie URL dla danego miesiąca
    url = f"https://www.kalbi.pl/kalendarz-swiat-nietypowych-{month_name.lower()}"
    
    # Wysyłanie żądania GET
    response = requests.get(url)

    # Sprawdzenie statusu odpowiedzi
    if response.status_code == 200:
        # Parsowanie HTML za pomocą BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Znalezienie wszystkich artykułów z nietypowymi dniami
        articles = soup.find_all('article', class_='unusual-day')
        
        for article in articles:
            # Parsowanie daty
            date_text = article.find('time').text.strip().split("\n")
            month = months[date_text[0].lower()]  # Miesiąc (np. styczeń -> 1)
            day = int(date_text[1].strip())  # Dzień (np. 3)
            
            # Znajdowanie wszystkich świąt w danym dniu
            descriptions = article.find_all('div', class_='description-of-holiday')
            
            for description in descriptions:
                # Nazwa święta
                name = description.find('h3').text.strip()
                # Link do szczegółowego opisu
                link = description.find('a')['href']
                
                # Sprawdzanie, czy jest element <p> z opisem
                holiday_info = description.find('p')
                if holiday_info:
                    holiday_info = holiday_info.text.strip()
                else:
                    holiday_info = "Brak opisu"
                
                # Dodajemy święto do listy
                holidays.append({
                    "day": day,
                    "month": month,
                    "name": name,
                    "link": link,
                    "description": holiday_info
                })
    else:
        print(f"Nie udało się pobrać strony: {url}. Kod odpowiedzi: {response.status_code}")

# Zapisanie do pliku JSON
with open("nietypowe_swieta.json", "w", encoding="utf-8") as file:
    json.dump(holidays, file, ensure_ascii=False, indent=4)

print("Dane zapisane do nietypowe_swieta.json")
