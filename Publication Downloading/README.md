# Publication Downloading
## Introduction of Publication Downloading
According to the DOI of each file, the program downloads the HTML content form the pulisher website.

## Dependency of Publication Downloading
* Node.js >= 12
* puppeteer
* winston

## Instructions of Publication Downloading
1. Make sure you install Node.js and added it into the system path.
1. install of the dependency:
   ```
    npm install puppeteer winston
   ```
1. run the script to show the instruction:
   ```
   node .\PublicationDownloading.js 
   ```

## Some problems inside Publication Downloading
1. The publishers updated their website and the loading process to provide a higher user experience. These changes may cause errors in reading the webpages of these publishers.
1. This program uses the headless browser Chromium built in puppeteer to load web pages. But sometimes the headless browser may fail, and it is possible to use the user's own chrome browser, or to set the headless browser to "false".




