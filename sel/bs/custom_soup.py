import os
import pathlib

import requests

# Set current working directory
cwd = str(pathlib.Path(__file__).parent.parent.absolute())


class Custom_Soup:
    """Class Custom_Soup is used to facilitate the use of BeautifulSoup methods"""

    def __init__(self, name, url):
        """[summary]

        Args:
            name (String): Webpage name
            url (String): URL of webpage
        """
        self.response = ""
        self.name = str(name)
        self.url = str(url)

    def get_text(self):
        """ Returns text of webpage based on HTTP response

        Returns:
            [string]: Text of webpage
        """
        if self.response != "":
            return self.response.text
        else:
            print(
                "Get page text error: No response object. Please run get_request function first")

    def download_page(self):
        """ Downloads HTML of website and saves to download folder """
        if self.response != "":
            if not os.path.isdir(cwd + "/downloads"):
                os.mkdir(cwd + "/downloads")
            with open(cwd + "/downloads/" + self.name + ".html", "w") as file:
                file.write(self.response.text)
        else:
            print(
                "Downloading page error: No response object. Please run get_request function first")

    def download_file(self):
        """ Downloads file and saves to download folder """
        file_extension = self.url.rsplit(".", 1)[1]
        print("file extension = " + file_extension)
        if not os.path.isdir(cwd + "/downloads"):
            os.mkdir(cwd + "/downloads")
        if self.response != "":
            with open(os.open(cwd + "/downloads/" + self.name + "." + file_extension, os.O_CREAT | os.O_WRONLY, 0o777), "wb") as file:
                file.write(self.response.content)
        else:
            print(
                "Downloading file error: No response object. Please run get_request function first")

    def get_request(self):
        """ Executes HTTP requests and saves response """
        response = requests.get(self.url)
        print("Response code for: " + str(response.status_code))
        self.response = response
