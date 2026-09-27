import os
from pathlib import Path

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()
SECRET = os.getenv("SECRET")

BASE_DIR = Path(__file__).resolve().parent

# Configure Chrome and use the bundled driver.
chrome_options = Options()
chrome_options.add_argument("--disable-search-engine-choice-screen")

prefs = {"download.default_directory": str(BASE_DIR)}
chrome_options.add_experimental_option("prefs", prefs)

service = Service(BASE_DIR / "downloads/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(options=chrome_options, service=service)
driver.get("https://demoqa.com/login")

# Wait until both login fields are ready for input.
username_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "userName"))
)
password_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "password"))
)
login_button = driver.find_element(By.ID, "login")

username_field.send_keys("pereira.oliver")
password_field.send_keys(SECRET)
driver.execute_script("arguments[0].click()", login_button)
WebDriverWait(driver, 10).until(EC.url_contains("/profile"))

# Locate the Elements dropdown and Text Box
elements = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div/div[1]/span/div')
    )
)
elements.click()

text_box = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Text Box']"))
)
text_box.click()

# Locate the form fields
fullname_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "userName"))
)
email_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "userEmail"))
)
current_address_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "currentAddress"))
)
permanent_address_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "permanentAddress"))
)

submit_button = driver.find_element(By.ID, "submit")

# Fill in the form fields

fullname_field.send_keys("Oliver Pereira")
email_field.send_keys("oliver@gmail.com")
current_address_field.send_keys("123 Main St, Anytown, USA")
permanent_address_field.send_keys("456 Oak Ave, Somewhere, USA")
driver.execute_script("arguments[0].click()", submit_button)

# Locate the Upload and Download section and the Download button
upload_download = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "item-7"))
)
upload_download.click()

download_button = driver.find_element(By.ID, "downloadButton")
driver.execute_script("arguments[0].click()", download_button)

# Keep the browser open until the user is finished inspecting it.
input("Press Enter to close the browser")
driver.quit()
