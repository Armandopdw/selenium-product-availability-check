import zipfile
import os
import pathlib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from sel.bs.custom_soup import Custom_Soup

# Sets current working directory
cwd = str(pathlib.Path(__file__).parent.absolute())


class Build_Selenium:
    def __init__(self, your_os, your_version, headless):
        """ Initiate Build Selenium class
        Args:
            your_os (str): Operating System. Possible values: mac, windows, linux
            your_version (str): Google Chrome Version
            headless (bool): Run Selenium headless
        """
        self.os_dict = {"mac": "mac64",
                        "windows": "win32",
                        "linux":  "linux64"}
        self.opso = self.os_dict[your_os.lower()]
        self.headless = headless
        self.version = str(your_version).rsplit(".", 1)[0]
        self.latest_release = ""
        self.chromedriver_path = str(cwd) + '/chromedriver'
        self.download_path = str(cwd)+'/downloads'
        self.chrome_options = webdriver.ChromeOptions()

    def get_latest_release(self):
        """ Get latest Chromedriver release based on Chrome version """
        cs = Custom_Soup(
            "latest_release", "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_" + str(self.version))
        cs.get_request()
        self.latest_release = cs.get_text()

    def download_chromedriver(self):
        """ Download chromedriver """
        # Download chromedriver based on operating system and latest chromedriver release
        cs = Custom_Soup("chromedriver", "https://chromedriver.storage.googleapis.com/" +
                         self.latest_release + "/chromedriver_" + self.opso + ".zip")
        cs.get_request()
        cs.download_file()
        file = zipfile.ZipFile(self.download_path + "/chromedriver.zip")
        if not os.path.isdir(self.chromedriver_path):
            os.mkdir(self.chromedriver_path)
        file.extractall(path=self.chromedriver_path)

    def return_driver(self):
        """ Sets Selenium options and returns driver

        Returns:
            [obj]: Selenium Driver
        """
        # Set UserAgent to prevent issues with blocking bot
        self.chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
        # Set headless
        if self.headless == True:
            self.chrome_options.add_argument('headless')
        # Initiate driver
        driver = webdriver.Chrome(
            self.chromedriver_path + "/chromedriver", options=self.chrome_options)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        return self.driver
