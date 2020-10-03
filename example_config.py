# config.py
class Config:
    # Navigate to chrome://version/ to see your Google Chrome Version
    CHROME_VERSION = "85.0.4183.121"
    # Possible options are "mac", "linux", "windows"
    OS_NAME = "mac"
    # Run Selenium headless
    HEADLESS = True
    # Your email address
    SENDER_EMAIL = "<email@gmail.com>"
    # Email address of recipient
    RECEIVER_EMAIL = "<email@gmail.com>"
    # Product name that you are interested in
    PRODUCT = "PS5"
    # URL of Product (Currently only El Corte Ingles Canarias supported)
    URL = "https://www.elcorteingles.es/canarias/videojuegos/A37046604/"
    # Plain text for your email
    PLAIN_TEXT = f"""\
    Hi,
    {PRODUCT} is finally back at El Corte Ingles!
    You should go to: {URL}
    Sent from automated Selenium Product Availability Check script.
    """
    # Formatted HTML for your email
    HTML = f"""\
    < html >
    <body >
        <p > Hi, < br >
        {PRODUCT} is finally back at El Corte Ingles < br >
        You should go to: < a href = "{URL}" > El Corte Ingles < /a > <br >
        Sent from automated Selenium Product Availability Check script.
        </p >
    </body >
    </html >
    """