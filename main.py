# main.py
from loguru import logger as lg

# Try to import config file
try:
    from config import Config
except ModuleNotFoundError as e:
    raise RuntimeError(
        "config.py file has not been set yet, adjust and rename the example_config.py")

from mail.mail import Mail

from sel.build_selenium import CustomSelenium

if __name__ == '__main__':
    lg.info("Building Selenium..")
    # Build selenium with Custom Selenium Class
    cust_sel = CustomSelenium(Config.OS_NAME, Config.CHROME_VERSION,
                              headless=Config.HEADLESS)

    # Initiate driver
    driver = cust_sel.driver

    lg.info("Opening: %s" % Config.URL)
    # Navigate to URL
    driver.get(Config.URL)
    # Accept cookie banner
    cust_sel.click_element(".js-modal-footer-accept")

    lg.info("Checking status..")
    # Obtain inner text
    inner_text = cust_sel.get_inner_text(".js-buy-button")

    # Agotado = Sold Out. Will send email if product is back
    if inner_text != "AGOTADO":
        lg.info("Product is available!")

        # Initiate mail server
        ml = Mail(Config.SENDER_EMAIL, Config.RECEIVER_EMAIL)
        ml.create_ssl_connection()
        ml.load_password()

        lg.info("Sending mail to: %s" % Config.RECEIVER_EMAIL)
        # Send email
        ml.send_email(f"{Config.PRODUCT} is Back!",
                      Config.PLAIN_TEXT, Config.HTML)
    else:
        lg.info("Product is unavailable")

    lg.info("Done with Main thread")
