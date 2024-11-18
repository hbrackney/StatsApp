# StatsApp
CSCI 6118 Project - Statistics Learning Web App 


## Installation 
Download package. All specific dependencies are  included in the ` environment.yaml` file. Create environment with required dependencies using the `environment.yaml` file: 
```
conda env create -f environment.yaml
```

## Usage
From command line or in visual studio terminal, run the server.py file: 
```
python app.py
``` 
Go to your preferred browser and enter 
```
localhost:14000
```
The website is now live! 

To end the website run and to regain typing ability in command line or terminal press `Crtl + C`. 

## Changelog
18-11-2024 (HB): Filled in Reference page to explain more and be more of a template.
18-11-2024 (HB): Added a figure on the home page that flips between images from some of the pages.
18-11-2024 (HB): Added python and R examples to Distributions Page. Added code/precode styles to the styles.css file. 
12-11-2024 (SS): Added quiz to z-test page and added more thorough docstrings. <br>
11-11-2024 (HB): Added Distribution Page with tests for the dash apps and plots. <br/>
06-11-24 (SS): Added example python script to z-test page and updated about page. <br/>

### Version 0
This version is an initial build to test basic functions and usablity. </br>
</br>
30-10-2024 (LS): Added and fixed tests in the test_dash_apps.py through dash.testing. </br>
30-10-2024 (HB): Removed t_quiz.py/quizzes.py (and corresponding test files). Corrected quiz code in t-test.html. Added tests for dash_apps.py and plots.py</br>
30-10-2024 (SS): Updated data tabes and plots for z-test page so that an updated box plot, z-statistic value, and p-value are correctly displayed when the user inputs new data points into the table. </br>
25-10-2024 (HB): Spilt app.py into app.py, dash_apps.py, plots.py to make things easier to read. </br>
25-10-2024 (SS): Added z-test example info to the z-test page </br>
23-10-2024 (HB): Added a knowledge quiz to the t-test page<br/>
23-10-2024 (HB): Added tests for app initialization <br/>
23-10-2024 (HB): Added a navigation bar <br/>
23-10-2024 (SS): Fixed formatting errors on z-test page <br>
21-10-2024 (SS): Added z-test text information <br/>
21-10-2024 (LS): Added t-test text information with images and updated general formatting <br/>
16-10-2024 (HB): Added interactive plots to the content pages (t test, z test, example page) <br/>
07-10-2024 (HB): Changed type entry box to dropdown menu for users <br/>
07-10-2024 (HB): Added "Return Home" button to each page <br/>
07-10-2024 (HB): Created template html files to create inital GUI <br/>
07-10-2024 (HB): Created server.py file to create web app <br/>
