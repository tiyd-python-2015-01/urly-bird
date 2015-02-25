# URLy Bird API

## How to run requests

* To see a list of all bookmarks (regardless of user):
  * curl http://localhost:5000/api/v1/bookmarks
* To see a specific bookmark:
  * curl http://localhost:5000/api/v1/bookmarks
* To add a bookmark:
  * curl -X POST -H "Authorization: Basic zackjcooper@gmail.com:password" -H "Content-type: application/json" -d '{"description": "super social", "title": "Instagram", "url": "http://www.instagram.com/"}' http://localhost:5000/api/v1/bookmarks
