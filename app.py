from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, jsonify, request
import ipdb

app = Flask(__name__)

def fetch_amazon_data():
    options = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    options.add_argument(f'user-agent={user_agent}')
        # #options.add_argument("--headless")
    options.add_argument("--headless=new")
    options.add_argument("--lang=en-IN")
    options.add_experimental_option('prefs', {
      'intl.accept_languages': 'en-IN'
    })
    options.add_argument("--no-sandbox")
    options.add_argument("--single-process")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("--disable-extensions")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get("https://www.amazon.in")
        wait = WebDriverWait(driver, 10)

        # Search for "lg soundbar"
        search_box = wait.until(EC.presence_of_element_located((By.ID, "twotabsearchtextbox")))
        search_box.send_keys("lg soundbar")
        search_box.submit()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot")))

        products = {}

        # Find product names and prices on the first search results page
        product_elements = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div.s-result-item")

        for product in product_elements:
            try:
                # Fetch product name
                name = product.find_element(By.CSS_SELECTOR, "h2 a span").text
                try:
                    price_whole = product.find_element(By.CSS_SELECTOR, ".a-price-whole").text
                    price = f"{price_whole}"
                except:
                    price = "0"

                # Clean and store the price as an integer
                products[name] = int(price.replace(',', ''))

            except Exception as e:
                print(f"Error processing product: {e}")

        sorted_products = sorted(products.items(), key=lambda item: item[1])

        # Prepare results
        result_list = [f"{price} {name}" for name, price in sorted_products]

    finally:
        driver.quit()

    return result_list

@app.route('/')
def main():
    results = fetch_amazon_data()

    # Print results
    for result in results:
        print(result)

    # Write sorted results to file
    with open('output.txt', 'w') as file:
        for result in results:
            file.write(result + "\n")

    return jsonify({"results": results})

if __name__ == '__main__':
    app.run()
