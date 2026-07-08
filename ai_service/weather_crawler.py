import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import httpx

# =====================================================================
# CONFIGURATION
# =====================================================================
LOCATION = "ho-chi-minh-city"
START_YEAR = 2023
END_YEAR = 2026

# Output filenames
CSV_OUTPUT_PATH = "hcm_weather_history.csv"

# =====================================================================
# METHOD 1: CRAWL VIA OPEN-METEO API (100% Reliable, Free, Fast)
# =====================================================================
def get_weather_via_open_meteo():
    """
    Open-Meteo has full historical weather for Ho Chi Minh City from 1940-present.
    This method downloads the data via API in seconds, without any block.
    """
    print("\n--- [Method 1] Fetching Weather via Open-Meteo API (TP.HCM) ---")
    
    # Lat/Long for Ho Chi Minh City
    lat = 10.823
    lon = 106.6296
    
    url = f"https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": f"{START_YEAR}-01-01",
        "end_date": "2026-07-01",
        "hourly": "temperature_2m,relative_humidity_2m,rain,surface_pressure,cloud_cover,wind_speed_10m,wind_gusts_10m",
        "timezone": "Asia/Bangkok"
    }
    
    try:
        print("Sending request to Open-Meteo...")
        response = httpx.get(url, params=params, timeout=30)
        if response.status_code != 200:
            print(f"Error fetching from Open-Meteo: {response.status_code}")
            return None
            
        data = response.json()
        hourly_data = data.get("hourly", {})
        
        if not hourly_data:
            print("No hourly data returned.")
            return None
            
        # Convert to DataFrame
        df = pd.DataFrame({
            "datetime": hourly_data.get("time"),
            "temperature": hourly_data.get("temperature_2m"),
            "humidity": hourly_data.get("relative_humidity_2m"),
            "rain": hourly_data.get("rain"),
            "pressure": hourly_data.get("surface_pressure"),
            "cloud": hourly_data.get("cloud_cover"),
            "wind": hourly_data.get("wind_speed_10m"),
            "gust": hourly_data.get("wind_gusts_10m")
        })
        
        print(f"Successfully retrieved {len(df)} rows from Open-Meteo!")
        return df
        
    except Exception as e:
        print(f"Failed to fetch from Open-Meteo: {e}")
        return None

# =====================================================================
# METHOD 2: CRAWL VIA WORLDWEATHERONLINE (Selenium Scraper)
# =====================================================================
def get_weather_via_selenium():
    """
    Uses Selenium to click through years and months on the WorldWeatherOnline
    historical weather page and parses the weather tables.
    """
    print("\n--- [Method 2] Crawling WorldWeatherOnline via Selenium ---")
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        driver = webdriver.Chrome(options=options)
    except Exception as e:
        print(f"Could not initialize Chrome Webdriver: {e}")
        print("Please check that Google Chrome and chromedriver are installed on your system.")
        return None
        
    url = f"https://www.worldweatheronline.com/{LOCATION}-weather-history/vn.aspx"
    all_records = []
    
    try:
        print(f"Opening initial page: {url}")
        driver.get(url)
        time.sleep(3)
        
        for year in range(START_YEAR, END_YEAR + 1):
            for month in range(1, 13):
                # We stop if we reach the future (current time is July 2026)
                if year == 2026 and month > 7:
                    break
                    
                print(f"Crawling Weather for {month:02d}/{year}...")
                
                try:
                    # Select Month
                    month_el = Select(driver.find_element(By.ID, "ctl00_MainContentHolder_drpMonth"))
                    month_el.select_by_value(str(month))
                    
                    # Select Year
                    year_el = Select(driver.find_element(By.ID, "ctl00_MainContentHolder_drpYear"))
                    year_el.select_by_value(str(year))
                    
                    # Click Button to show weather
                    btn = driver.find_element(By.ID, "ctl00_MainContentHolder_butShowYear")
                    btn.click()
                    
                    time.sleep(3)  # Wait for page to refresh and load data
                    
                    # Parse the page
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    
                    # Look for weather history table
                    # Usually under a table with class 'table-responsive' or table tags
                    tables = soup.find_all('table')
                    table_found = False
                    
                    for table in tables:
                        # Inspect table class or headers
                        headers = [th.text.strip().lower() for th in table.find_all('th')]
                        if any("temp" in h or "weather" in h or "wind" in h for h in headers):
                            # This is the target weather data table
                            rows = table.find_all('tr')[1:] # Skip header
                            for row in rows:
                                cols = [td.text.strip() for td in row.find_all('td')]
                                if len(cols) >= 5:
                                    all_records.append({
                                        "year": year,
                                        "month": month,
                                        "data": cols
                                    })
                            table_found = True
                            break
                            
                    if not table_found:
                        print(f"WARNING: No weather table found for {month:02d}/{year}")
                        
                except Exception as ex:
                    print(f"Error scraping {month:02d}/{year}: {ex}")
                    continue
                    
        print(f"Selenium crawling finished. Found {len(all_records)} records.")
        if all_records:
            return pd.DataFrame(all_records)
        return None
        
    finally:
        driver.quit()

# =====================================================================
# MAIN RUNNER
# =====================================================================
if __name__ == "__main__":
    print("=== InfoAgent System - Weather Crawler ===")
    
    # 1. Try Method 1 first (Open-Meteo API) since it's 100% reliable and doesn't get blocked
    df = get_weather_via_open_meteo()
    
    # 2. If Open-Meteo fails, fall back to Method 2 (Selenium WWO Scraper)
    if df is None:
        print("Open-Meteo failed. Falling back to WorldWeatherOnline Selenium Scraper...")
        df = get_weather_via_selenium()
        
    # 3. Save result to CSV
    if df is not None:
        df.to_csv(CSV_OUTPUT_PATH, index=False)
        print(f"\nSUCCESS: Dataset saved to '{CSV_OUTPUT_PATH}'")
        print(df.head())
    else:
        print("\nFATAL: Both scraping methods failed. Please check your internet connection or package versions.")
