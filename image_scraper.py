import os
import time
import requests
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
from io import BytesIO

def download_image(url, save_dir, index, downloaded_images):
    try:
        response = requests.get(url, stream=True, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content)).convert('RGB')
        img_path = os.path.join(save_dir, f"image_{index+1}.jpg")
        img.save(img_path, quality=95)
        downloaded_images[index] = img_path
    except Exception as e:
        print(f"❌ Failed to download image {index+1} from {url}: {e}")
        downloaded_images[index] = None

def search_and_download_images(query, num_images=5):
    # Set up headless Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    search_url = f"https://www.bing.com/images/search?q={query}&qft=+filterui:imagesize-large"
    driver.get(search_url)

    # Scroll to load more images
    for _ in range(5):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
        time.sleep(2)

    image_elements = driver.find_elements(By.CSS_SELECTOR, "img.mimg")
    image_urls = []

    for img in image_elements:
        src = img.get_attribute('src') or img.get_attribute('data-src')
        if src and src.startswith('http'):
            image_urls.append(src)
        if len(image_urls) >= num_images:
            break

    driver.quit()

    save_dir = os.path.abspath(query.replace(' ', '_'))
    os.makedirs(save_dir, exist_ok=True)

    downloaded_images = [None] * len(image_urls)
    threads = []

    for i, url in enumerate(image_urls):
        thread = threading.Thread(target=download_image, args=(url, save_dir, i, downloaded_images))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Filter out failed downloads
    return [img for img in downloaded_images if img is not None]

# Example usage
if __name__ == "__main__":
    images = search_and_download_images("mars rover", num_images=5)
    print("✅ Downloaded images:", images)
