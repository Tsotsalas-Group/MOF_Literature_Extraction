
# literature Extraction
## Introduciton of literature Extraction
In this part we show the process of how scientific literature is extracted to generate 
a table of the synthesis conditions. 

![MOF Literature Extraction](https://github.com/Tsotsalas-Group/MOF_Literature_Extraction/blob/main/Literature%20Extraction/Extraction%20Process.png)

This part is written in Python.

## Dependency of literature Extraction
* python 3.7
* ...
  
Also needs java in your OS:
* java 6.5


## File descirption
* Code: All python script for literature extraction
```
Code
├─cd_lib
│  ├─chetg            # inout and output for chemicaltagger
│  ├─chose_para       # Paragraph classification
│  ├─csd_api          # some functions of CSD API
│  ├─csv_cond         # read the result of chemicaltagger
│  ├─pcplib           # modified pubchempy
│  ├─post_processing  # functions related to the database
├─cd_tools
│  ├─csvalkyrie       # customized csv operation functions, suitable for cold backup
│  ├─osvalkyrie       # some system operation functions
│  └─ToHTML           # Database operation functions
├─DemoDatabase        # A demo database for literature extraction demo
└─_CommonRedist       # some necessary files
```
    
* Databases: the database we extracted for Machine Learning:
  * SynMOF_A:   983 entries of MOF synthesis conditions based on automatical extraction
  * SynMOF_ME:  880 entries of MOF synthesis conditions
  * SynMOF_M:   880 entries of MOF synthesis conditions



