
# literature Extraction
## Introduciton of literature Extraction
In this part we show the process of how scientific literature is extracted to generate 
a table of the synthesis conditions. 

![MOF Literature Extraction](https://github.com/Tsotsalas-Group/MOF_Literature_Extraction/blob/main/Literature%20Extraction/Extraction%20Process.png)

This part is written in Python.

## Dependency of literature Extraction
* python 3.7
* pandas
* chemdataextractor
* numpy
* html5lib
* xlrd
* pubchempy
* jupyterlab
* nltk
* unidecode
* theano
  
Also needs java in your OS:
* java

## Installation of Dependency
For java, one of the easies ways to install java is https://www.java.com/

it is recommended to use conda to install all the python dependency
1. create and activate a new environment
```
conda create -n [env name] python=3.7 -y
conda activate [env name]

```
2. install dependency
```
conda install pandas -y
conda install -c conda-forge chemdataextractor numpy theano nltk jupyterlab -y
conda install -c anaconda html5lib xlrd unidecode -y
conda install -c bioconda pubchempy -y
```

3. open the demo
```
cd "[root_of_MOF_literature_Extraction]/Literature Extraction/Code"
jupyter notebook LiteratureExtractionDemo.ipynb
```

## File descirption
* Code: All python script for literature extraction
```
Code
├─cd_lib
│  ├─chetg            # inout and output for chemicaltagger
│  ├─chose_para       # paragraph classification
│  ├─csd_api          # some functions of CSD API
│  ├─csv_cond         # read the result of chemicaltagger
│  ├─pcplib           # modified pubchempy
│  ├─post_processing  # functions related to the database
├─cd_tools
│  ├─csvalkyrie       # customized csv operation functions, suitable for cold backup
│  ├─osvalkyrie       # some system operation functions
│  └─ToHTML           # database operation functions
├─_CommonRedist       # some necessary files
└─DemoDatabase        # a demo database for LiteratureExtractionDemo.ipynb
```
    
* Databases: the database we extracted for Machine Learning:
  * SynMOF_A:   983 entries of MOF synthesis conditions based on automatical extraction
  * SynMOF_ME:  841 entries of MOF synthesis conditions based on manually extraction
  * SynMOF_M:   841 entries of MOF synthesis conditions
  



