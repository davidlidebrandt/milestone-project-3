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

[Link to the deployed project](https://movie-r-and-r.herokuapp.com/)

# Table Of Contents

* [Database](#datbase)
* [UX](#ux)
* [Features](#features)
* [Technologies Used](#technologies-used)
* [Testing](#testing)
* [Deployment](#deployment)
* [Credits](#credits)

## Database

The database chosen for the project is MongoDB which is a NoSQL database. The two main enteties stored in the
datbase are users and movies. The user entety stores the username, password, email and an admin
check for different users. All of the fields are stored in simple key value pairs.
The movies entety stores data in both simple key value pairs and in a nested structure.
The simple key value pairs that will be stored are title, director, rating, year and image URL
Reviews are stored in an array as a nested object with the key value pairs of author and description.
Cast is stored as an array of names and the has rated entety stores values of user names that has already 
rated a particular movie in an array.


## UX




### User Stories

#### Regular user

* As a user I want access to others reviews and rating of relevant movies.

* As a user I want to be able to write my own reviews and add my own ratings.

* As a user I want to be able to edit and delete my own reviews.

* As a user I want to option to search for movies as well as being able to scroll through a selection of movies.

* As a user I want a clear response to my actions such as adding, deleting and editing my reviews.

* As a user I want navigation to be clear and consistent across the website.

* As a user I want the top rated movies to be displayed when visiting the website.

#### Administrative user

* As an administrator I want to be able to add new movies to the database.

* As an administrator I want to be able to edit already added movies.

* As an administrator I want to be able to delete reviews made by other users.


#### Wireframes and Mockups

* [Wireframe Mobile](/images/wireframes-mockups/wireframe-mobile.png)
* [Wireframe Tablet](/images/wireframes-mockups/wireframe-tablet.png)
* [Wireframe Desktop](/images/wireframes-mockups/wireframe-desktop.png)

* [Mockup Mobile](/images/wireframes-mockups/mockup-mobile.png)
* [Mockup Tablet](/images/wireframes-mockups/mockup-tablet.png)
* [Mockup Desktop](/images/wireframes-mockups/mockup-desktop.png)
   

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
https://www.pexels.com/photo/abstract-analog-art-camera-390089/


### Acknowledgments

