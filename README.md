# Milestone Project 2

<img src=""
     alt=""
     style="height: 200px; width: 400px;" />
     
<img src=""
     alt=""
     style="height: 200px; width: 400px;" />

<img src=""
     alt=""
     style="height: 200px; width: 400px;" />

<img src=""
     alt=""
     style="height: 200px; width: 400px;" />

 This project is intended to provide a service for movie ratings and reviews. Users can search for different movies
 and read reviews and see ratings by other users. By registering and loggin in a user can add their own reviews and
 ratings as well as edit and delete old reviews they have made in the past.



[Link to the deployed project]()

* [Database](#datbase)
* [UX](#ux)
* [Features](#features)
* [Technologies Used](#technologies-used)
* [Testing](#testing)
* [Deployment](#deployment)
* [Credits](#credits)

## Database

The database chosen for the project is MongoDB which is a NoSQL database. The two main enteties stored in the
datbase will be users and movies. The user entety will simply store the username and password for different users 
so that users can log in and add and manage their reviews. 
The movies entety will store both simple key value pairs but will also have a nested structure where objects will
be stored inside it. The simple key value pairs that will be stored are title, director, rating and year, cast will be 
stored as a nested object with the key value pair of name. The reviews will be stored a a nested object with the 
key value pairs of author and description. 

users:  {"Object_id: "", "username": "", "password": ""}

movies: {"Object_id": "", "title": "", "director": "", "rating": "", "year": "", "cast": {"Object_id": "", "name": ""}, 
"reviews": {"Object_id": {"author":"", "description": ""}}}

## UX



### User Stories

* As a user I want access to others reviews and rating of relevant movies.

* As a user I want to be able to write my own reviews and add my own ratings.

* As a user I want to be able to edit and delete my own reviews.

* As a user I want to option to search for movies as well as being able to scroll through a selection of movies.

* As a user I want a clear response to my actions such as adding, deleting and editing my reviews.

* As a user I want navigation to be clear and consistent across the website.

* As a user I want the top rated movies to be displayed when visiting the website.



#### Wireframes and Mockups

* [Wireframe Mobile]()
* [Wireframe Tablet]()
* [Wireframe Desktop]()

* [Mockup Mobile]()
* [Mockup Tablet]()
* [Mockup Desktop]()
   

## Features

### Existing Features

#### Index page



#### Game page




### Future Features



## Technologies Used

* HTML

For the basic structure of the web page.

* CSS

For the styling of the HTML elements.

* JavaScript

To add interactivity to the project.

* [JQuery](https://jquery.com/)

JQuery functions where used to manipulate the DOM and to take actions.

* [Bootstrap](https://getbootstrap.com/)



* [Google Fonts](https://fonts.google.com/)



* [Github](https://github.com/)

Github was used to store the repository.

* [Gitpod](https://www.gitpod.io/)

Gitpod was the IDE used to create the project.

* [Git](https://git-scm.com/) 

For version control through the gitpod terminal.

* [Adobe XD](https://www.adobe.com/products/xd.html)

Adobe XD was used to create the wireframes and mockups for the project.

* [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools)

Chrome DevTools was heavily used throughout the project,  mainly by debugging and testing with help of the console and
checking the responsiveness of the page with their screen rendering tools.

* http://whatismyscreenresolution.net/multi-screen-test 

For testing the responsiveness across different devices.

## Testing



### Bugs



## Deployment

### Publishing the project


### Forking the project
1. Go to and log in to https://github.com/.
2. Go to the repository: https://github.com/davidlidebrandt/milestone-project-2
3. Press the fork button located on the right side.
4. Make your changes to the project.
5. If you wish to merge your changes to the original project:
6. Press the pull request button from your forked repository.
7. Press the button new pull request.
8. Choose the branches you wish to merge.
9. Press the Create pull request button.

### Cloning the project
There are several ways of cloning the project, here I am going to describe how to do it using
the URL and Git Bash.
1. Go to the repository: https://github.com/davidlidebrandt/milestone-project-2
2. Click the Code button.
3. Choose HTTPS and copy the link that is provided.
4. Open Git Bash and navigate to the directory where you want to save the cloned project.
5. Type git clone followed by the url you copied, git clone https://github.com/davidlidebrandt/milestone-project-2.git

## Credits 

### Content



### Media



### Acknowledgments

