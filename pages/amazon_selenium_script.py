from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode for no GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open Amazon.in
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


print("\nAll products and their prices:")
for name, price in products.items():
    print(f"Product: {name}, Price: {price}")


sorted_products = sorted(products.items(), key=lambda item: item[1])

# Write sorted results to file and print them
with open('output.txt', 'w') as file:
    print("\nSorted products by price:")
    for name, price in sorted_products:
        result = f"{price} {name}"
        print(result)
        file.write(result + "\n")

driver.quit()
