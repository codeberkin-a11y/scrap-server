#!/usr/bin/env python3
"""
Local test script for Nesine Scraper Logic
Tests the scraping functions directly
"""

import json
import sys
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

def setup_driver():
    """Setup Chrome WebDriver for testing"""
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

def scrape_matches(sport, date):
    """Main scraping logic - direct port from API"""
    driver = setup_driver()
    
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

def test_scraper():
    """Test the scraper logic locally"""
    try:
        print("🔧 Testing scraper logic...")
        
        # Test today's matches
        today = datetime.now().strftime('%d.%m.%Y')
        matches = scrape_matches('futbol', today)
        
        print(f"📊 Found {len(matches)} matches for today ({today})")
        
        if matches:
            print("🎮 Sample match:")
            print(json.dumps(matches[0], indent=2, ensure_ascii=False))
            print("\n🏆 First 3 matches:")
            for i, match in enumerate(matches[:3], 1):
                print(f"{i}. {match.get('saat', '')} - {match.get('mac', 'Unknown')} - MBS: {match.get('mbs', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Starting Nesine Scraper Logic Test")
    print("=" * 40)
    
    success = test_scraper()
    
    print("=" * 40)
    if success:
        print("🎉 Scraper logic works! API is ready for deployment.")
    else:
        print("💥 Tests failed. Check the error messages above.")
    
    exit(0 if success else 1)