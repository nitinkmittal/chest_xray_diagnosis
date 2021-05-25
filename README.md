# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###

* Summary of set up
* Configuration
* Dependencies
* Database configuration
* How to run tests
* Deployment instructions

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact



### SetUp Commands ###
```bash
conda env create -f environment.yml
conda activate chest_xray_diagnosis
pip install kaggle
kaggle competitions download -c vinbigdata-chest-xray-abnormalities-detection
```

### Data ###
To directly download the data from kaggle use [link](https://www.kaggle.com/c/vinbigdata-chest-xray-abnormalities-detection/data)`