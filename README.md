<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** 

-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/Armandopdw/selenium-product-availability-check">
    <img src="images/selenium_logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Selenium Product Availability Check</h3>

  <p align="center">
    A package that uses Selenium to check product availability for El Corte Ingles Webshop. Package can be edited to work for any webshop.
    <br />
    <a href="https://github.com/Armandopdw/selenium-product-availability-check"><strong>Explore the docs »</strong></a>
    <br />
    ·
    <a href="https://github.com/Armandopdw/selenium-product-availability-check/issues">Report Bug</a>
    ·
    <a href="https://github.com/Armandopdw/selenium-product-availability-check/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/Armandopdw/selenium-product-availability-check/images/screenshot.png)

### Built With

* [Python 3](https://www.python.org/downloads/)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use this package and how to install them.
* wget
```sh
$ apt install wget
```
* Google Chrome (Linux)
```sh
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
```



### Installation

1. Clone the repo
```sh
$ git clone https://github.com/Armandopdw/selenium-product-availability-check.git
```
2. Install required Python packages
```sh
$ pip install .
```
3. Enter configuration settings in `config.py`
```py
# Navigate to chrome://version/ to see your Google Chrome Version
CHROME_VERSION = "85.0.4183.121"
# Possible options are "mac", "linux", "windows"
OS_NAME = "linux"
# After running main.py for the first time set to True
CHROMEDRIVER_DOWNLOADED = False
# Your email address
SENDER_EMAIL = "<email@gmail.com>"
# Email address of recepient
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
<html>
<body>
    <p>Hi,<br>
    {PRODUCT} is finally back at El Corte Ingles<br>
    You should go to: <a href="{URL}">El Corte Ingles</a> <br>
    Sent from automated Selenium Product Availability Check script.
    </p>
</body>
</html>
"""
```
4. Enter your email password in `mail/pw/pw.txt`
```txt
<Password>
```
5. Run main.py
```sh
$ python3 main.py
```



<!-- USAGE EXAMPLES -->
## Usage

After running main.py you will either receive an email that the product is available again, or nothing will happen. Complete package can be installed on a virtual machine (e.g. Compute Engine in Google Cloud Platform) for hourly check of availability. See below the step by step walkthrough to have this code run every hour on a Google Cloud Compute Engine:


### Step 1: Create Compute Engine Instance

Standard settings will suffice
_For more info, please refer to the [GCP Documentation](https://cloud.google.com/compute/docs/instances/create-start-instance)_

### Step 2: Upload file to the compute engine instance

Upload by using the UI in the top right corner, or by uploading it to a GCP bucket and running the following command 
```sh
gsutil cp gs://my-bucket/selenium-product-availability-check.zip .
apt install unzip
unzip selenium-product-availability-check.zip
```

### Step 3: Unzip file & install packages

By default our Compute Engine will not have unzip installed, so it install this package and unzip the uploaded file
```sh
$ apt install unzip
$ unzip selenium-product-availability-check.zip
$ pip install .
```

### Step 4: Install Chrome

Selenium requires Google Chrome to be installed, so run the following commands
```sh
$ apt install wget
$ wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
$ dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
```

### Step 5: Set up Cron Job

If we want main.py to run hourly, you will need to set up a Cron Job. The following line will result in main.py to run every time the virtual machine is booted. Step 6 will explain how you can schedule the start and stop of your Virtual Machine. For more information check [Documentation](https://www.cyberciti.biz/faq/how-do-i-add-jobs-to-cron-under-linux-or-unix-oses/)
```sh
crontab -e
```

Add the following line in the Crontab, this will make sure the script runs every hour on the first minute. 
```txt
@reboot {user} python3 /home/{user-name}/main.py
```

### Step 6: Set up Google Cloud Scheduler
To reduce the use of the virtual machine (and thereby the costs) you want to turn it off when it is not running the script. 
Therefore, you should use Google Cloud Scheduler. Follow the instructions in the following [Documentation](https://cloud.google.com/scheduler/docs/start-and-stop-compute-engine-instances-on-a-schedule). The aforementioned instructions will start and stop an instance based on its labels. However, you want to specifically start and stop the relevant virtual machine. Therefore, you need to change the Node JS script slightly.

#### Obtain instance ID & instance zone
Go to your Compute Engine instance and note the Instance ID and zone.

#### Edit startInstancePubSub function
Edit the index.js of the startInstancePubSub function. 
```js
const Compute = require('@google-cloud/compute');
const compute = new Compute();

/**
 * Starts Compute Engine instances.
 *
 * Expects a PubSub message with JSON-formatted event data containing the
 * following attributes:
 *  zone - the GCP zone the instances are located in.
 *  id - the id of instances to start.
 *
 * @param {!object} event Cloud Function PubSub message event.
 * @param {!object} callback Cloud Function PubSub callback indicating
 *  completion.
 */
exports.startInstancePubSub = async (event, context, callback) => {
  try {
    const payload = _validatePayload(
      JSON.parse(Buffer.from(event.data, 'base64').toString())
    );
    const options = {filter: `id = ${payload.id}`};
    const [vms] = await compute.getVMs(options);
    await Promise.all(
      vms.map(async (instance) => {
        if (payload.zone === instance.zone.id) {
          const [operation] = await compute
            .zone(payload.zone)
            .vm(instance.name)
            .start();

          // Operation pending
          return operation.promise();
        }
      })
    );

    // Operation complete. Instance successfully started.
    const message = `Successfully started instance(s)`;
    console.log(message);
    callback(null, message);
  } catch (err) {
    console.log(err);
    callback(err);
  }
};

/**
 * Validates that a request payload contains the expected fields.
 *
 * @param {!object} payload the request payload to validate.
 * @return {!object} the payload object.
 */
const _validatePayload = (payload) => {
  if (!payload.zone) {
    throw new Error(`Attribute 'zone' missing from payload`);
  } else if (!payload.id) {
    throw new Error(`Attribute 'id' missing from payload`);
  }
  return payload;
};
```

#### Edit stopInstancePubSub function
Edit the index.js of the stopInstancePubSub function. 
```js
const Compute = require('@google-cloud/compute');
const compute = new Compute();

/**
 * Stops Compute Engine instances.
 *
 * Expects a PubSub message with JSON-formatted event data containing the
 * following attributes:
 *  zone - the GCP zone the instances are located in.
 *  id - the id of instances to stop.
 *
 * @param {!object} event Cloud Function PubSub message event.
 * @param {!object} callback Cloud Function PubSub callback indicating completion.
 */
exports.stopInstancePubSub = async (event, context, callback) => {
  try {
    const payload = _validatePayload(
      JSON.parse(Buffer.from(event.data, 'base64').toString())
    );
    const options = {filter: `id = ${payload.id}`};
    const [vms] = await compute.getVMs(options);
    await Promise.all(
      vms.map(async (instance) => {
        if (payload.zone === instance.zone.id) {
          const [operation] = await compute
            .zone(payload.zone)
            .vm(instance.name)
            .stop();

          // Operation pending
          return operation.promise();
        } else {
          return Promise.resolve();
        }
      })
    );

    // Operation complete. Instance successfully stopped.
    const message = `Successfully stopped instance(s)`;
    console.log(message);
    callback(null, message);
  } catch (err) {
    console.log(err);
    callback(err);
  }
};

/**
 * Validates that a request payload contains the expected fields.
 *
 * @param {!object} payload the request payload to validate.
 * @return {!object} the payload object.
 */
const _validatePayload = (payload) => {
  if (!payload.zone) {
    throw new Error(`Attribute 'zone' missing from payload`);
  } else if (!payload.id) {
    throw new Error(`Attribute 'id' missing from payload`);
  }
  return payload;
};
```

#### Obtain Base64 encoding
Google Pub Sup requires base64 encoded data. Go to a [base64-encoder](https://www.base64encode.net/) and encode the following text
``` json
{"zone":"{ZONE}", "id":"{VIRTUAL MACHINE INSTANCE ID}"}
```

#### Add message to Pub Sub Topic
Using the base64 encoded string add the following message to your Pub Sub Topic
``` json
{"data":"{BASE64ENCODED"}
```




<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/Armandopdw/selenium-product-availability-check/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Armando Panman de Wit  - armando.panmandewit@artlytic.nl

Project Link: [https://github.com/Armandopdw/selenium-product-availability-check](https://github.com/Armandopdw/selenium-product-availability-check)




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Armandopdw/repo.svg?style=flat-square
[contributors-url]: https://github.com/Armandopdw/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Armandopdw/repo.svg?style=flat-square
[forks-url]: https://github.com/Armandopdw/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/Armandopdw/repo.svg?style=flat-square
[stars-url]: https://github.com/Armandopdw/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/Armandopdw/repo.svg?style=flat-square
[issues-url]: https://github.com/Armandopdw/repo/issues
[license-shield]: https://img.shields.io/github/license/Armandopdw/repo.svg?style=flat-square
[license-url]: https://github.com/Armandopdw/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/Armandopdw
[product-screenshot]: images/screenshot.png
