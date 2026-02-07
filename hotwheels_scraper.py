"""
Hot Wheels Database Scraper for collecthw.com

This script scrapes Hot Wheels car data from collecthw.com and exports it to JSON/CSV
that can be imported into your collection app.

Requirements:
    pip install requests beautifulsoup4 selenium pandas --break-system-packages

Note: collecthw.com may block automated requests. This script includes:
1. User-agent headers to mimic browser requests
2. Rate limiting to be respectful
3. Option to use Selenium for JavaScript-rendered content
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
from datetime import datetime
import random

class HotWheelsScraper:
    def __init__(self):
        self.base_url = "https://collecthw.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.cars = []
        
    def scrape_cars(self, max_pages=5):
        """
        Scrape cars from the website
        """
        print(f"Starting scrape of {self.base_url}...")
        
        try:
            # Try to get the main page first
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            print(f"Successfully connected to {self.base_url}")
            
            # You'll need to inspect the HTML structure of collecthw.com
            # and adjust these selectors accordingly
            # This is a template - actual selectors depend on the site structure
            
            car_elements = soup.find_all('div', class_='car-item')  # Example selector
            
            for car_elem in car_elements:
                try:
                    car_data = self._extract_car_data(car_elem)
                    if car_data:
                        self.cars.append(car_data)
                        print(f"Scraped: {car_data['name']}")
                except Exception as e:
                    print(f"Error extracting car data: {e}")
                    continue
                
                # Rate limiting - be respectful
                time.sleep(random.uniform(1, 3))
            
            print(f"\nTotal cars scraped: {len(self.cars)}")
            
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to website: {e}")
            print("\nThe website may be blocking automated requests.")
            print("Try using Selenium with a real browser (see scrape_with_selenium method)")
            
    def _extract_car_data(self, element):
        """
        Extract car data from HTML element
        Adjust selectors based on actual HTML structure
        """
        try:
            car = {
                'id': element.get('data-id', f'hw-{int(time.time())}'),
                'name': element.find('h3', class_='car-name').text.strip(),
                'series': element.find('span', class_='series').text.strip() if element.find('span', class_='series') else '',
                'year': element.find('span', class_='year').text.strip() if element.find('span', class_='year') else '',
                'color': element.find('span', class_='color').text.strip() if element.find('span', class_='color') else '',
                'manufacturer': 'Mattel',
                'category': element.find('span', class_='category').text.strip() if element.find('span', class_='category') else '',
                'imageUrl': element.find('img')['src'] if element.find('img') else '',
                'notes': ''
            }
            return car
        except Exception as e:
            print(f"Error parsing car element: {e}")
            return None
    
    def scrape_with_selenium(self):
        """
        Alternative scraping method using Selenium for JavaScript-rendered content
        Requires: pip install selenium
        """
        try:
            from selenium import webdriver
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.chrome.options import Options
            
            chrome_options = Options()
            chrome_options.add_argument('--headless')  # Run in background
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument(f'user-agent={self.headers["User-Agent"]}')
            
            driver = webdriver.Chrome(options=chrome_options)
            
            print("Loading page with Selenium...")
            driver.get(self.base_url)
            
            # Wait for content to load
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "car-item")))
            
            # Scroll to load all content (if infinite scroll)
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            car_elements = soup.find_all('div', class_='car-item')
            
            for car_elem in car_elements:
                car_data = self._extract_car_data(car_elem)
                if car_data:
                    self.cars.append(car_data)
                    print(f"Scraped: {car_data['name']}")
            
            driver.quit()
            print(f"\nTotal cars scraped: {len(self.cars)}")
            
        except ImportError:
            print("Selenium not installed. Install with: pip install selenium")
        except Exception as e:
            print(f"Selenium error: {e}")
    
    def manual_data_entry(self):
        """
        If scraping doesn't work, you can manually add cars
        """
        print("\n=== Manual Car Entry ===")
        while True:
            print("\nEnter car details (or press Enter on name to finish):")
            name = input("Car Name: ").strip()
            if not name:
                break
                
            car = {
                'id': f'manual-{int(time.time())}',
                'name': name,
                'series': input("Series: ").strip(),
                'year': input("Year: ").strip(),
                'color': input("Color: ").strip(),
                'manufacturer': input("Manufacturer (default: Mattel): ").strip() or 'Mattel',
                'category': input("Category: ").strip(),
                'imageUrl': input("Image URL (optional): ").strip(),
                'notes': input("Notes (optional): ").strip()
            }
            self.cars.append(car)
            print(f"Added: {car['name']}")
    
    def export_to_json(self, filename='hotwheels_database.json'):
        """Export scraped data to JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.cars, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Exported {len(self.cars)} cars to {filename}")
    
    def export_to_csv(self, filename='hotwheels_database.csv'):
        """Export scraped data to CSV"""
        if not self.cars:
            print("No cars to export!")
            return
            
        keys = self.cars[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.cars)
        print(f"✅ Exported {len(self.cars)} cars to {filename}")
    
    def generate_javascript_array(self, filename='hotwheels_database.js'):
        """Generate JavaScript array for direct use in HTML app"""
        js_content = f"""// Hot Wheels Database
// Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

const HOTWHEELS_DATABASE = {json.dumps(self.cars, indent=2)};

// To use in your app:
// Replace the SAMPLE_DATABASE constant with HOTWHEELS_DATABASE
"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(js_content)
        print(f"✅ Exported {len(self.cars)} cars to {filename}")
        print("\nTo use this in your app:")
        print("1. Open hotwheels-collection-enhanced.html")
        print("2. Find the SAMPLE_DATABASE constant")
        print("3. Replace it with the contents of hotwheels_database.js")


def main():
    scraper = HotWheelsScraper()
    
    print("Hot Wheels Database Scraper")
    print("="*50)
    print("\nOptions:")
    print("1. Try scraping with requests (may be blocked)")
    print("2. Try scraping with Selenium (requires Chrome)")
    print("3. Manual data entry")
    print("4. Use sample database (quit)")
    
    choice = input("\nSelect option (1-4): ").strip()
    
    if choice == '1':
        scraper.scrape_cars()
    elif choice == '2':
        scraper.scrape_with_selenium()
    elif choice == '3':
        scraper.manual_data_entry()
    else:
        print("Using sample database provided in the app.")
        return
    
    if scraper.cars:
        print("\nExport options:")
        print("1. JSON (for backend integration)")
        print("2. CSV (for spreadsheet editing)")
        print("3. JavaScript (for direct use in HTML app)")
        print("4. All formats")
        
        export_choice = input("\nSelect export format (1-4): ").strip()
        
        if export_choice == '1':
            scraper.export_to_json()
        elif export_choice == '2':
            scraper.export_to_csv()
        elif export_choice == '3':
            scraper.generate_javascript_array()
        elif export_choice == '4':
            scraper.export_to_json()
            scraper.export_to_csv()
            scraper.generate_javascript_array()


if __name__ == "__main__":
    main()
