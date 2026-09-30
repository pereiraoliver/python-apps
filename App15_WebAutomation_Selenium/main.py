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


class WebAutomation:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent

        chrome_options = Options()
        chrome_options.add_argument("--disable-search-engine-choice-screen")
        chrome_options.add_experimental_option(
            "prefs", {"download.default_directory": str(self.base_dir)}
        )

        service = Service(
            self.base_dir / "downloads/chromedriver-win64/chromedriver.exe"
        )
        self.driver = webdriver.Chrome(options=chrome_options, service=service)
        self.wait = WebDriverWait(self.driver, 10)

    def login(self, username, password):
        self.driver.get("https://demoqa.com/login")

        username_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "userName"))
        )
        password_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "password"))
        )
        login_button = self.driver.find_element(By.ID, "login")

        username_field.send_keys(username)
        password_field.send_keys(password)
        self.driver.execute_script("arguments[0].click()", login_button)
        self.wait.until(EC.url_contains("/profile"))

    def open_text_box(self):
        elements = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="root"]/div/div/div/div[1]/div/div/div[1]/span/div')
            )
        )
        elements.click()

        text_box = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[normalize-space()='Text Box']")
            )
        )
        text_box.click()

    def fill_text_box(self, full_name, email, current_address, permanent_address):
        fullname_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "userName"))
        )
        email_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "userEmail"))
        )
        current_address_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "currentAddress"))
        )
        permanent_address_field = self.wait.until(
            EC.visibility_of_element_located((By.ID, "permanentAddress"))
        )

        fullname_field.send_keys(full_name)
        email_field.send_keys(email)
        current_address_field.send_keys(current_address)
        permanent_address_field.send_keys(permanent_address)

        submit_button = self.driver.find_element(By.ID, "submit")
        self.driver.execute_script("arguments[0].click()", submit_button)

    def download_file(self, folder=None):
        download_dir = Path(folder) if folder is not None else self.base_dir
        download_dir.mkdir(parents=True, exist_ok=True)
        self.driver.execute_cdp_cmd(
            "Page.setDownloadBehavior",
            {"behavior": "allow", "downloadPath": str(download_dir)},
        )

        upload_download = self.wait.until(
            EC.visibility_of_element_located((By.ID, "item-7"))
        )
        upload_download.click()

        download_button = self.driver.find_element(By.ID, "downloadButton")
        self.driver.execute_script("arguments[0].click()", download_button)

    def run(
        self,
        username,
        password,
        full_name,
        email,
        current_address,
        permanent_address,
    ):
        self.login(username, password)
        self.open_text_box()
        self.fill_text_box(full_name, email, current_address, permanent_address)
        self.download_file()

    def close(self):
        self.driver.quit()


def main():
    automation = WebAutomation()
    try:
        automation.run(
            username="pereira.oliver",
            password=os.getenv("SECRET"),
            full_name="Oliver Pereira",
            email="oliver@gmail.com",
            current_address="123 Main St, Anytown, USA",
            permanent_address="456 Oak Ave, Somewhere, USA",
        )
        input("Press Enter to close the browser")
    finally:
        automation.close()


if __name__ == "__main__":
    main()
