# Application Structure
## Overview
The application has a client-server-database structure, with multiple pages and mainly static content. The application consists of different views that are calculated on the server, fetched, and then rendered to the user. There are also some asyncronous features, and the application is developed to a more asyncronous direction.

## Technology/Libraries
The application is coded in Python, JavaScript, HTML and CSS.

The main libraries used are:
  * Flask
  * Flask-SQLAlchemy
  * Flask-WTF
  * Jinja2
  
## Database Structure
Currently, the application uses SqLite in the development environment and PostqreSQL in Heroku. The database implementation will almost certainly change in the future.

## Module Structure
The surface structure of the application
![](https://github.com/LauriTahvanainen/GameTracker/blob/master/documentation/pictures/module_structure.png)

The server can be thought of as consisting of modules, each representing one object handled by the application. This structure is based extensively on the database structure, and the insides of the modules are more complex than just representing the object and have different types of functions.

For example, the observation module would consist of every method for each view, meaning all the functions responsible for saving, fetching data and doing calculations on data. It consists also of all the templates, and the instructions to fill the templates correctly with the information gotten from the view functions. The template defines the final page returned to the user. The observation module consists also of all the different forms in the application that are needed for handling observation-input.
All the modules have a depency on the LoginManager, which handles user authentication on each view. The modules also have dependencies to each other, but all these dependencies emerge from the database structure, so they are not examined here.
Javascript and html are used on the client for input and dynamic responses. Some data manipulation is also handled in javascript for better performance. For example, the voting system is implemented so that the given votes are structured into arrays and json-format, and the request for saving the votes is sent only when the user leaves or refreshes the page.
