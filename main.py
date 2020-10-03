# main.py
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from config import Config
from sel.build_selenium import Build_Selenium
from mail.mail import Mail


def wait_for_element(css_selector):
    """ Function for Selenium driver to wait for element to be clickable

    Args:
        css_selector (String): CSS Selector for element
    """
    se.wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, css_selector)))


def click_element(css_selector):
    """ Function for Selenium driver to click on element after waiting for it to be clickable

    Args:
        css_selector ([type]): CSS Selector for element
    """
    wait_for_element(css_selector)
    driver.find_element_by_css_selector(css_selector).click()


def get_inner_text(css_selector):
    """ Function for Selenium driver to obtain inner text of element

    Args:
        css_selector ([type]): CSS Selector for element
    """
    element = driver.find_elements_by_css_selector(css_selector)
    if len(element) > 0:
        information = element[0].get_attribute("innerText").strip()
    return information


# Build selenium
se = Build_Selenium(Config.OS_NAME, Config.CHROME_VERSION,
                    headless=Config.HEADLESS)
# Prevents repreated download of chromedriver
if Config.CHROMEDRIVER_DOWNLOADED != True:
    # get latest release of chromedriver
    se.get_latest_release()
    # download latest release of chromedriver
    se.download_chromedriver()

# Initiate driver
driver = se.return_driver()
# Navigate to URL
driver.get(Config.URL)
# Accept cookie banner
click_element(".js-modal-footer-accept")
# Obtain inner text
inner_text = get_inner_text(".js-buy-button")

# Initiate mail server
ml = Mail(Config.SENDER_EMAIL, Config.RECEIVER_EMAIL)
ml.create_ssl_connection()
ml.load_password()

# Agotado = Sold Out. Will send email if product is back
if inner_text != "AGOTADO":
    ml.send_email(f"{Config.PRODUCT} is Back!", Config.PLAIN_TEXT, Config.HTML)
