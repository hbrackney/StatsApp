# StatsApp
CSCI 6118 Project - Statiscs Learning Web App 

## Installation 
Download package. Create environment with required dependencies using the environment.yaml file ("conda env create -f environment.yaml"). Flask may require additional download in the conda environment.

## Usage
From command line or in visual studio terminal, run the server.py file ("python app.py"). Go to your preferred browser and enter "localhost:8000". The website is now live! 

To end the website run and to regain typing ability in command line or terminal press Crtl + C. 

## Changelog
30-10-2024 (SS): Updated data tabes and plots for z-test page so that an updated box plot, z-statistic value, and p-value are correctly displayed when the user inputs new data points into the table. <br>
25-10-2024 (HB): Spilt app.py into app.py, dash_apps.py, plots.py to make things easier to read. <br>
25-10-2024 (SS): Added z-test example info to the z-test page <br>
23-10-2024 (HB): Added a knowledge quiz to the t-test page -> NOT WORKING YET (failing all tests)<br/>
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
