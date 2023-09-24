from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time

# URL of the product's review page on Daraz Bangladesh
url = "https://www.daraz.com.bd/products/4in1-double-part-inflatable-travelling-pillow-set-with-eye-mask-ear-plug-pouch-air-inflated-is-soft-and-comfortable-materials70-pvc-30-velvet-i103354537-s1447405727.html?spm=a2a0e.home.flashSale.3.557012f7TTqkGN"

# Set up the Selenium webdriver (you need to install the appropriate driver, e.g., chromedriver)
driver = webdriver.Chrome()

# Load the page
driver.get(url)
time.sleep(5)  # Allow time for the page to load

# Scroll down to load more reviews (adjust the number of scrolls as needed)
num_scrolls = 5
for _ in range(num_scrolls):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# Get the page source after scrolling
page_source = driver.page_source

# Close the Selenium webdriver
driver.quit()

# Parse the page source using BeautifulSoup
soup = BeautifulSoup(page_source, "html.parser")

# Lists to store review data
review_texts = []
ratings = []

# Find the HTML elements containing the reviews
review_elements = soup.find_all("div", class_="mod-reviews-item")

for review in review_elements:
    review_text = review.find("div", class_="content").get_text(strip=True)
    rating_text = review.find("div", class_="star-inner")["style"]
    rating_value = int(rating_text.split(":")[1].split("%")[0]) / 20  # Convert % to a 5-star scale

    review_texts.append(review_text)
    ratings.append(rating_value)

# Create a DataFrame to store the data
data = {
    "Rating": ratings,
    "Review": review_texts
}
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
excel_file = "daraz_product_reviews.xlsx"
df.to_excel(excel_file, index=False, engine="openpyxl")

print(f"Reviews extracted and saved to {excel_file}")
