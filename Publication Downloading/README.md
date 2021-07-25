# MOF_Literature_Extraction
## Introduction
The programs extract the MOF synthesis information from literature devided into 2 parts:
* Publication Downloading
* Literature Extraction
The first part is in Node.js and second part in developed in Python.
  

## Publication Downloading
### Introduction of Publication Downloading
According to the DOI of each file, the program downloads the HTML content form the pulisher website.

### Dependency of Publication Downloading
* Node.js >= 12
* puppeteer
* winston

### Instructions of Publication Downloading
1. Make sure you install Node.js and added it into the system path.
1. install of the dependency:
   ```
    npm install puppeteer winston
   ```
1. run the script to show the instruction:
   ```
   node .\PublicationDownloading.js 
   ```

### Some problems inside Publication Downloading
1. The publisher's website has been working to update their pages and the loading process  to provide a higher user experience. These new changes will cause errors in the reading of the web pages of some publishers.
1. This program uses the headless browser Chromium built in puppeteer to load web pages. But sometimes the headless browser may fail, and it is possible to use the user's own chrome browser, or to set the headless browser to "false".




