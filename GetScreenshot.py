from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import datetime
import os


class GetScreenshot:
    def __init__(self):
        self.element_xpath = '//*[@id="__next"]/main/div/div[2]/a'
        self.chrome_options = Options()
        self.chrome_options.add_argument(
            "--no-sandbox --disable-dev-shm-usage --disable-renderer-backgrounding --incognito"
            "--disable-background-timer-throttling --disable-backgrounding-occluded-windows"
            "--disable-client-side-phishing-detection --disable-crash-reporter --disable-oopr-debug-crash-dump"
            "--no-crash-upload --disable-gpu --disable-extensions --disable-low-res-tiling --log-level=3 --silent")
        # self.chrome_options.add_argument("--headless=new")
        self.driver = webdriver.Chrome(options=self.chrome_options)

        self.screenshot_dir = "element_screenshots"

    def get_video_screenshot(self, source_url, source_name, delay):
        self.driver.get(source_url)
        sleep(delay)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"element_screenshots/{source_name}-{timestamp}.png"

        element = self.driver.find_element(By.XPATH, self.element_xpath)
        element.screenshot(filename)

        self.driver.quit()

    def get_latest_screenshot(self, source_name):

        source_files = [f for f in os.listdir(self.screenshot_dir) if source_name in f]
        sorted_files = sorted(source_files, key=lambda f: os.path.getmtime(os.path.join(self.screenshot_dir, f)))
        if sorted_files:
            latest_file = sorted_files[-1]
            latest_path = os.path.join(self.screenshot_dir, latest_file)
            return latest_path
        else:
            return None

    def fetch_objects_in_screenshot(self):
        pass


if __name__ == "__main__":
    video_url = "https://www.pexels.com/video/an-artist-painting-of-the-carpenter-s-son-4166533/"
    watchdog = GetScreenshot()
    watchdog.get_video_screenshot(video_url, "pexelsvideo01", 4)

    last_ss_path = watchdog.get_latest_screenshot("pexelsvideo01")
    if last_ss_path:
        print(31)
    else:
        print("Kayit bulunamadı kiral")
