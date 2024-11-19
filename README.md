# BioStat Academy
CSCI 6118 Project - An interactive app designed to introduce basic statistical concepts to biologists. Learning statistics is crucial for biologists, as it enables them to analyze data, design reliable experiments, and draw valid conclusions. Statistics is essential in concepts like hypothesis testing and biological variability, as well as making evidence-based decisions. With statistical tools, biologists can interpret results accurately, manage large datasets, and communicate findings effectively. Thus, learning and understanding statistics is important for all research biologists.

## Installation 
Clone the repository in your command line by:
```
git clone https://github.com/hbrackney/StatsApp.git
```
 All specific dependencies are included in the ` environment.yaml` file. Create environment with required dependencies using the `environment.yaml` file: 
```
conda env create -f environment.yaml
```
And then activate the environment:
```
conda activate StatsApp
```
Step into the repository by: (for Mac or Windows users)
```
cd StatsApp 
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
19-11-2024 (HB): Changed ReadME.md installation instructions to be more through. <br/>
19-11-2024 (HB): Fixed Quiz on Distributions Page. Added more tests for plots.py and app.py. <br/>
18-11-2024 (LS): Updated and expanded README and CONTRIBUTING to include background info and description. <br/>
18-11-2024 (HB): Filled in Reference page to explain more and be more of a template. <br/>
18-11-2024 (HB): Added a figure on the home page that flips between images from some of the pages. <br/>
18-11-2024 (HB): Added python and R examples to Distributions Page. Added code/precode styles to the styles.css file. <br/>
12-11-2024 (SS): Added quiz to z-test page and added more thorough docstrings. <br/>
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
