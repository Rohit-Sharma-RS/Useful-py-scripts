import time
import csv
import re
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def scrape_restaurant_data(region, output_file):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        search_query = f"restaurants in {region}"
        driver.get("https://www.google.com")
        search_box = driver.find_element(By.NAME, "q")
        search_box.send_keys(search_query + Keys.RETURN)
        time.sleep(3)

        restaurant_data = []

        try:
            more_places_button = driver.find_element(By.CSS_SELECTOR, "span.Z4Cazf.OSrXXb")
            more_places_button.click()
            time.sleep(2)
        except Exception as e:
            print(f"Error clicking 'More places' button: {e}")

        while True:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            restaurant_blocks = soup.find_all('div', class_='VkpGBb')

            for block in restaurant_blocks:
                try:
                    name = block.find('div', class_='dbg0pd').text.strip()
                    rating_block = block.find('span', class_='Y0A0hc')
                    rating = rating_block.find('span', class_='yi40Hd YrbPuc').text.strip() if rating_block else "N/A"
                    reviews = rating_block.find('span', class_='RDApEe YrbPuc').text.strip().strip('()') if rating_block else "N/A"

                    # Extract Address and Expense Level
                    details_text = block.text
                    cost_match = re.search(r"\u00b7 ([$₹]+)\s?", details_text)
                    address_match = re.search(r"\u00b7 ([$₹]+)?\s?(.*?)(Closed|Opens|Dine-in|\u22c5|$)", details_text)

                    expense_level = "Moderate Cost"  # Default
                    if cost_match:
                        expense_level = cost_match.group(1)
                        if expense_level.startswith("$"):
                            expense_value = expense_level.replace("$", "").replace("+", "").split("–")
                            if len(expense_value) == 1:
                                expense_value = float(expense_value[0])
                            else:
                                expense_value = float(expense_value[1])
                            if expense_value <= 20:
                                expense_level = "Low Cost"
                            elif expense_value <= 40:
                                expense_level = "Moderate Cost"
                            else:
                                expense_level = "Expensive"
                        elif expense_level == "₹":
                            expense_level = "Low Cost"
                        elif expense_level == "₹₹":
                            expense_level = "Moderate Cost"
                        elif expense_level == "₹₹₹":
                            expense_level = "Expensive"
                        elif expense_level == "₹₹₹₹":
                            expense_level = "Very Expensive"
                    else:
                        expense_level = "Moderate Cost"

                    address = address_match.group(2).strip() if address_match and address_match.group(2) else "N/A"
                    if "·" in address:
                        address = address.split("·")[1].strip()

                    restaurant_data.append({
                        "Name": name,
                        "Rating": rating,
                        "Reviews": reviews,
                        "Address": address,
                        "Expense Level": expense_level
                    })
                except Exception as e:
                    print(f"Error extracting data for a restaurant block: {e}")

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "a#pnnext")
                next_button.click()
                time.sleep(2)
            except Exception:
                print("No more pages to scrape.")
                break

        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Name", "Rating", "Reviews", "Expense Level", "Address"])
            writer.writeheader()
            writer.writerows(restaurant_data)

        print(f"Data successfully saved to {output_file}.")

    finally:
        driver.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape restaurant data from Google.")
    parser.add_argument("--region", required=True, help="The region to search for restaurants.")
    parser.add_argument("--output", required=True, help="The output CSV file to save the restaurant data.")
    args = parser.parse_args()

    scrape_restaurant_data(args.region, args.output)
