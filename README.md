# swapp
#### Description:
This is a web application for swapping your unused items which i made both for cs50 final project and preparation for my future projects

[View the full assignment description](https://cs50.harvard.edu/x/2023/project/)

## Technologies
* Python
* Flask with session authentication
* SQLite3
* HTML
* CSS


## What I've done

I've wrote all the functions except login (from prev. project) at app.py by using **python, flask and sql** , wrote all the html files templates folder by using **html and jinja**, and wrote style.css by using **css**.

## How to Run
* Clone this repository, navigate to the project and type the following commands:
* Activate a virtual environment: 'python3 -m venv .venv' then select the virtual environment as the active workspace
* Install dependencies: 'pip install -r requirements.txt'
* Install 'pip install psycopg2' or 'pip install psycopg2-binary'
* Run command 'export FLASK_APP=application.py' to set the Flask environment variable
* Configure and export your API key with these instructions
* Run command 'flask run' to open on localhost
* When the finance site opens in your browser, register for a new account (upper right corner) to create your own stock portfolio

* run: sqlite3 swapp.db and
* CREATE TABLE upload (
 	id INTEGER PRIMARY KEY AUTOINCREMENT,
 	user_id INTEGER NOT NULL,
    username TEXT NOT NULL;
 	title VARCHAR ( 100 ) NOT NULL,
 	name TEXT NOT NULL,
 	brand TEXT NOT NULL,
 	color TEXT NOT NULL,
 	condition TEXT NOT NULL);

* CREATE TABLE users (
 	id INTEGER PRIMARY KEY AUTOINCREMENT,
 	username TEXT NOT NULL,
 	hash TEXT NOT NULL);

## Explanation
Initially, user needs to register to our site by providing username which is not taken and a password. 

After this, user's username and password will be saved in the database. Then user needs to log in by providing user's correct username and pass.

After logging in user encounters with the index page where all the items in the database are shown with the information item's owner, photo, brand, condition and color.

There is a my_items page in which user can see their items and an area that has big addition sign which says "Append an item". This sign redirects the user to the sell page.

On the sell page, user can upload an item, by providing the item's name, brand, color , and condition. After uploading, site redirects the user to the my_items page again and saying "Item successfully uploaded and displayed below"

Lastly, there is a search page which can be improved. Now, it can just filter the items by color and condition. By improvements, it can be searched by all the features of the item, username and relevance.

