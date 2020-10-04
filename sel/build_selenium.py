import glob
import os
import pathlib
import zipfile

from loguru import logger as lg
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from sel.bs.custom_soup import Custom_Soup

# Sets current working directory
cwd = str(pathlib.Path(__file__).parent.absolute())


class CustomSelenium:
    OS_MAPPER = {"mac": "mac64",
                 "windows": "win32",
                 "linux": "linux64"}

    def __init__(self, your_os, your_version, headless, rebuild=False):
        """ Initiate Build Selenium class

        Args:
            your_os (str): Operating System. Possible values: mac, windows, linux
            your_version (str): Google Chrome Version
            headless (bool): Run Selenium headless
            rebuild (bool): Whether to rebuild (i.e. redownload) chromedriver
        """
        self.driver = None
        self.wait = None
        self.opso = self.OS_MAPPER[your_os.lower()]
        self.headless = headless
        self.version = str(your_version).rsplit(".", 1)[0]
        self.latest_release = ""
        self.chromedriver_path = str(cwd) + '/chromedriver'
        self.download_path = str(cwd) + '/downloads'
        self.chrome_options = webdriver.ChromeOptions()

        # Rebuild if forced or if no chromedriver exists yet
        nr_chromedriver_files = glob.glob(
            os.path.join(self.download_path, "*"))
        if rebuild or nr_chromedriver_files == 0:
            lg.debug("Rebuilding..")
            self.get_latest_release()
            self.download_chromedriver()
        else:
            lg.debug("Chromedriver already downloaded, so no need for rebuilding")

        self.init_driver()

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

    def init_driver(self):
        """ Sets Selenium options and returns driver

        Returns:
            [obj]: Selenium Driver
        """
        # Set UserAgent to prevent issues with blocking bot
        self.chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36")
        # Set headless
        if self.headless:
            self.chrome_options.add_argument('headless')
        # Initiate driver
        driver = webdriver.Chrome(
            self.chromedriver_path + "/chromedriver", options=self.chrome_options)
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)
        return self.driver

    def click_element(self, css_selector):
        """ Function for Selenium driver to click on element after waiting for it to be clickable

        Args:
            css_selector ([type]): CSS Selector for element
        """
        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, css_selector)))
        self.driver.find_element_by_css_selector(css_selector).click()

    def get_inner_text(self, css_selector):
        """ Function for Selenium driver to obtain inner text of element

        Args:
            css_selector ([type]): CSS Selector for element
        """
        element = self.driver.find_elements_by_css_selector(css_selector)
        if len(element) > 0:
            information = element[0].get_attribute("innerText").strip()
        return information
