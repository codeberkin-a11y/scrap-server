from http.server import BaseHTTPRequestHandler
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

class handler(BaseHTTPRequestHandler):
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        """Handle POST requests for scraping"""
        try:
            # Parse request body
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            sport = request_data.get('sport', 'futbol')
            date = request_data.get('date', datetime.now().strftime('%d.%m.%Y'))
            
            print(f"📡 Vercel API Request: {sport} - {date}")
            
            # Direct scraping implementation
            matches = self._scrape_matches(sport, date)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'matches': matches,
                'count': len(matches),
                'sport': sport,
                'date': date,
                'status': 'success'
            }
            
            self.wfile.write(json.dumps(response).encode('utf-8'))
                
        except Exception as e:
            print(f"❌ API Error: {str(e)}")
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            error_response = {
                'error': 'Scraping failed',
                'message': str(e),
                'status': 'error'
            }
            
            self.wfile.write(json.dumps(error_response).encode('utf-8'))
    
    def _setup_driver(self):
        """Setup Chrome WebDriver for Vercel"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        try:
            # Try to use ChromeDriverManager for automatic driver management
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
        except Exception:
            # Fallback to system chrome
            driver = webdriver.Chrome(options=chrome_options)
            
        return driver

    def _scrape_matches(self, sport, date):
        """Main scraping logic"""
        driver = self._setup_driver()
        
        try:
            # Build URL
            base_url = 'https://www.nesine.com/iddaa'
            
            if sport == 'basketbol':
                url = f"{base_url}/basketbol?dt={date}"
            else:
                url = f"{base_url}?dt={date}"
                
            print(f"🔍 Scraping: {url}")
            
            driver.get(url)
            time.sleep(3)
            
            # Wait for matches to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-code]'))
            )
            
            # Parse page
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            match_divs = soup.select('div[data-code][data-nid][data-sport-id]')
            
            print(f"📊 Found {len(match_divs)} match containers")
            
            matches = []
            for div in match_divs:
                try:
                    kod = div.get('data-code', '')
                    
                    # Time
                    time_elem = div.select_one('span[data-testid^="time"]')
                    saat = time_elem.get_text(strip=True) if time_elem else ''
                    
                    # Teams
                    name_elem = div.select_one('a[data-test-id="matchName"]')
                    mac = name_elem.get_text(strip=True) if name_elem else ''
                    
                    # MBS
                    mbs_elem = div.select_one('[data-test-id="event_mbs"] span')
                    mbs = mbs_elem.get_text(strip=True) if mbs_elem else ''
                    
                    # Odds
                    odds = {'odd_1': '', 'odd_x': '', 'odd_2': '', 'under_odd': '', 'over_odd': ''}
                    odd_buttons = div.select('button[data-testid^="odd_"]')
                    
                    for btn in odd_buttons:
                        testid = btn.get('data-testid', '')
                        value = btn.get_text(strip=True)
                        
                        if 'Maç Sonucu' in testid:
                            if testid.endswith('_1'):
                                odds['odd_1'] = value
                            elif testid.endswith('_X'):
                                odds['odd_x'] = value
                            elif testid.endswith('_2'):
                                odds['odd_2'] = value
                    
                    if kod and mac:
                        match = {
                            'kod': kod,
                            'saat': saat,
                            'mac': mac,
                            'mbs': mbs,
                            'spor': sport.title(),
                            **odds
                        }
                        matches.append(match)
                        
                except Exception as e:
                    print(f"⚠️ Match parsing error: {e}")
                    continue
            
            print(f"✅ Successfully parsed {len(matches)} matches")
            return matches
            
        finally:
            driver.quit()
    def do_GET(self):
        """Handle GET requests - health check"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'status': 'OK',
            'service': 'Nesine Scraper API',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat()
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))