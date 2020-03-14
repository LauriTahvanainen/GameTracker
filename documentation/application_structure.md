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

## More on the implementation of some individual features

### Voting

Like mentioned above, voting is handled with javascript on the client, and python on the server. 

When the user loads the view where the voting can be done, the existing votes of the user are loaded into set variables.

When the user clicks on the voting buttons, sets of suggestion_ids (animal id) are filled and emptied according to the given votes. For example, when the user gives an upvote to an suggestion, the id of the suggestion is added to the set named UpVotes.

The votes are handled and sent to the server only when the page is refreshed, another page is loaded, or the browser is closed. 

On these actions, the sets with the existing down- and upvotes and the sets with the votes given by the user on the current view are used to calculate the information that needs to be updated on the server. The calculations are simple set operations. By doing the calculation on the browser in advance, only the relevant information is sent to the server. 

The browser also does some simple checks to make sure the arrays are the of the right size.

On the server side, there are checks to make sure, that there are not more votes than suggestions etc. The arrays are also turned again to sets, so that possible multiples of votes are deleted.

All the cases that can happen with the votes given by the user are taken in to account and the votes are saved. If the amount of votes for one suggestions goes over or under the limits, the suggestion is either accepted or deleted accordingly. The amount of accepted or deleted animals are returned to the user.
