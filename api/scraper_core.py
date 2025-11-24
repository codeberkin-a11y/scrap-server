from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time


def _setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception:
        driver = webdriver.Chrome(options=chrome_options)

    return driver


def scrape_matches_for_date(sport, date_str):
    """Scrape matches for a given sport and date string (DD.MM.YYYY).
    Returns list of match dicts with an extra `match_date` key equal to date_str.
    """
    driver = _setup_driver()
    try:
        base_url = "https://www.nesine.com/iddaa"

        if sport == "basketbol":
            url = f"{base_url}/basketbol?dt={date_str}"
        else:
            url = f"{base_url}?dt={date_str}"

        driver.get(url)
        time.sleep(3)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-code]"))
        )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        match_divs = soup.select("div[data-code][data-nid][data-sport-id]")

        matches = []
        for div in match_divs:
            try:
                kod = div.get("data-code", "")

                time_elem = div.select_one('span[data-testid^="time"]')
                saat = time_elem.get_text(strip=True) if time_elem else ""

                name_elem = div.select_one('a[data-test-id="matchName"]')
                mac = name_elem.get_text(strip=True) if name_elem else ""

                mbs_elem = div.select_one('[data-test-id="event_mbs"] span')
                mbs = mbs_elem.get_text(strip=True) if mbs_elem else ""

                odds = {"odd_1": "", "odd_x": "", "odd_2": "", "under_odd": "", "over_odd": ""}
                odd_buttons = div.select('button[data-testid^="odd_"]')

                for btn in odd_buttons:
                    testid = btn.get("data-testid", "")
                    value = btn.get_text(strip=True)

                    if "Maç Sonucu" in testid:
                        if testid.endswith("_1"):
                            odds["odd_1"] = value
                        elif testid.endswith("_X"):
                            odds["odd_x"] = value
                        elif testid.endswith("_2"):
                            odds["odd_2"] = value

                if kod and mac:
                    match = {
                        "kod": kod,
                        "saat": saat,
                        "mac": mac,
                        "mbs": mbs,
                        "spor": sport.title(),
                        "match_date": date_str,
                        **odds,
                    }
                    matches.append(match)

            except Exception:
                continue

        return matches

    finally:
        driver.quit()
