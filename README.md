# URLy Bird

## Description

Create a URL shortener/bookmarking site with Flask.

## Objectives

### Learning Objectives

After completing this assignment, you should understand:

* How to build simple applications in Flask

## Details

### Deliverables

* A Git repo called urly-bird containing at least:
  * `README.md` file explaining how to run your project
  * a `requirements.txt` file
  * a suite of tests for your project (on day 2)

### Requirements  

* Passing unit tests
* No PEP8 or Pyflakes warnings or errors

## Day 1

### Normal Mode

Create a Flask app with the following features:

* User registration
* User login
* User logout

You can have an index page that only shows the current logged in/logged out status and has links to each of these features.

### Hard Mode

In addition to the requirements from **Normal Mode**:

* Display the name of the user on the page
* Add Foundation and style your forms with it
* Start on the Bookmark model

## Day 2

### Normal Mode

Create forms in your application for logged in users to create bookmarks. Each bookmark should have a title, a URL, and an optional description. In addition, it should have a unique code -- something like "x1yrd3a" -- for each bookmark for use in looking it up later.

Create a route like "/b/\<code\>" that will redirect any user -- not just logged in users -- to the bookmark associated with that code. The route does not have to look just like the example.

On a logged in user's index page, they should see a list of the bookmarks they've saved in reverse chronological order. The bookmark links should use the internal short-code route, not the original URL.

Your application should have navigation. When a user is logged in, show their name in the navigation.

### Hard Mode

In addition to the requirements from **Normal Mode**:

* Make a page where users can see _everyone's_ bookmarks in reverse chronological order
* Add pagination to both the individual index page and the all bookmarks page
* Add editing of bookmarks and deletion of bookmarks
* Add a new model, Click, that records each click of a bookmark, including the user -- or an anonymous user if no one is logged in -- and the timestamp.


## Day 3

We are going to do two things today:

* Record bookmark clicks.
* Deploy to Heroku.

First, add a new model, Click, that records each click of a bookmark, including the user -- or an anonymous user if no one is logged in -- and the timestamp.

Second, convert your configuration over to using Flask-AppConfig and deploy your application to Heroku.

### Hard Mode

Besides just recording each click of a bookmark, record the IP address and User-Agent of each click.

Complete all hard mode tasks not completed from days 1 and 2.


## Day 4

For the rest of these tasks, you will need a good amount of click data. Create fake data for this. Numpy and Faker are useful libraries for creating your fake data.

Add a stats page to each link where you can see the traffic for that link for the last 30 days in a line chart.

Add an overall stats page for each user where you can see a table of your links by popularity and their number
of clicks over the last 30 days.

### Hard Mode

1. For your individual link stats pages, make a table of where the clicks for your links are coming from by country. Bonus -- display this on a map.

2. Add an option to the individual and group stats pages where you can see stats for the last week, last 30 days, last year, or all time.


## Day 5

Finish up everything from days 1-4 first.

Then refactor your application to use [Flask blueprints](http://flask.pocoo.org/docs/0.10/blueprints/).

Lastly, add an API to your application allowing users to view and create bookmarks with JSON.


## Additional Resources

* [Flask Skeleton](https://github.com/tiyd-python-2015-01/cookiecutter-flask). Use this at your own risk. It explains how to use it in the README.
<<<<<<< HEAD
* [Hashids](http://hashids.org/python/). These may be useful for creating short URLs.
=======
* [Hashids](http://hashids.org/python/). These may be useful for creating short URLs.
>>>>>>> 8e6999742050c07a4cd80b18b59431d9dc99ee66
