from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pickle
import os

# Replace these placeholders with your GitHub credentials
github_username = "cehvah@rosalinetaurus.co.uk"
github_password = "cehvah@rosalinetaurus.co.uk"

# GitHub login URL
github_url = "https://www.github.com"
github_login_url = "https://github.com/login"

# Provided URL
website_url = "https://mbeeboo.dev.cehvah.shipyard.host"

# Configure ChromeOptions
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")

# Create a Chrome WebDriver instance with configured options
driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=chrome_options)

try:
    # Visit github_url
    driver.get(github_url)

    # Check if the cookies.pkl file exists in the directory
    if os.path.exists("cookies.pkl"):
        # Load cookies if available
        try:
            print("Adding cookies and revisiting github_url...")
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                # Omit the "domain" attribute
                cookie.pop('domain', None)
                driver.add_cookie(cookie)
            driver.get(github_url)
        except (FileNotFoundError, pickle.UnpicklingError):
            print("Error loading cookies. Logging in...")

    else:
        print("No cookies found. Logging in...")

        # Visit GitHub login page
        driver.get(github_login_url)

        # Enter GitHub credentials
        username_input = driver.find_element(By.ID, "login_field")
        password_input = driver.find_element(By.ID, "password")

        username_input.send_keys(github_username)
        password_input.send_keys(github_password)
        password_input.send_keys(Keys.RETURN)

        # Wait for the login process to complete (you may need to adjust the wait time)
        time.sleep(30)

        # Save cookies for future use
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

        # Visit github_url again after adding cookies
        driver.get(github_url)

    # Now navigate to the provided URL after logging in
    driver.get(website_url)

    github_login_button = driver.find_element(By.LINK_TEXT, "Log in with GitHub")
    github_login_button.click()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser window regardless of whether an exception occurred or not
    driver.quit()
