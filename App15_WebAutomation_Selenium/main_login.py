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


# Keep the browser open until the user is finished inspecting it.
input("Press Enter to close the browser")
driver.quit()
