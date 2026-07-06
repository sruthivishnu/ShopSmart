import os
import time
import requests
import pandas as pd

from PIL import Image
from io import BytesIO

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException

# LOAD CSV
df = pd.read_csv("category_products_table.csv")

# TAKE FIRST 50 PRODUCTS
df = df.head(12673)

# CREATE IMAGE FOLDER
os.makedirs("static/images", exist_ok=True)

# EXISTING FILES
existing_files = os.listdir("static/images")

# CHROME OPTIONS
options = webdriver.ChromeOptions()

# SHOW BROWSER
# options.add_argument("--headless")

# OPEN CHROME
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

# STORE IMAGE PATHS
image_paths = []

# LOOP PRODUCTS
for index, row in df.iterrows():

    try:

        # PRODUCT NAME COLUMN
        product_name = row['product_name']

        print(f"\nSearching image for: {product_name}")

        # CREATE FILE NAME
        filename = (
            product_name
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )[:50] + ".jpg"

        # SKIP EXISTING IMAGES
        if filename in existing_files:

            print(f"Already exists: {filename}")

            image_paths.append(f"images/{filename}")

            continue

        # BING IMAGE SEARCH
        search_url = f"https://www.bing.com/images/search?q={product_name}"

        driver.get(search_url)

        # WAIT FOR PAGE LOAD
        time.sleep(3)

        # FIND IMAGES
        images = driver.find_elements(By.CSS_SELECTOR, "img.mimg")

        image_url = None

        # GET FIRST VALID IMAGE URL
        for img in images:

            src = img.get_attribute("src")

            if src and src.startswith("http"):

                image_url = src
                break

        # DOWNLOAD IMAGE
        if image_url:

            try:

                response = requests.get(
                    image_url,
                    timeout=10
                )

                # CHECK RESPONSE
                if response.status_code == 200:

                    # VALIDATE IMAGE
                    image = Image.open(
                        BytesIO(response.content)
                    )

                    # IMAGE PATH
                    filepath = f"static/images/{filename}"

                    # SAVE IMAGE
                    image.save(filepath)

                    image_paths.append(
                        f"images/{filename}"
                    )

                    print(f"Downloaded: {filename}")

                else:

                    print("Invalid response")

                    image_paths.append("")

            except Exception as e:

                print("Invalid image:", e)

                image_paths.append("")

        else:

            print("No image found")

            image_paths.append("")

        # SMALL DELAY
        time.sleep(2)

    except WebDriverException as e:

        print("Browser error:", e)

        image_paths.append("")

        # RESTART BROWSER
        try:
            driver.quit()
        except:
            pass

        time.sleep(5)

        driver = webdriver.Chrome(
            service=Service(
                ChromeDriverManager().install()
            )
        )
driver.quit()

print("\nDONE!")