# Package Tutoron: Future Work

## Overall pipeline
In `detect.py`, the Tutoron uses a regex to look for words in the web page's content. It looks to see if any of the words match a word in the list of packages that we support (see next item below).

In `explain.py`, we perform on-the-fly queries to the `fetcher` database as well as a simple HTTP request to get the data we need to display on the Tutoron. While developing, I noticed a slight lag in having the Tutoron display for `nodemailer`, when compared relatively to the other 4 Tutorons above it in the `home.html`.

## Support more packages
Update the list in `packages.py` with an actual list of packages that we have Tutoron support for. This should probably be programmatically pulled from a database eventually.

This list is used for detection of words in the HTML page that should be picked up for Tutorons. Right now, it looks for the word `nodemailer` and will display a Tutoron for only `nodemailer`.

## Update Django models as needed
`models.py` contains all Django models that we need for a package Tutoron. If we need to access other tables in the `fetcher` database, we may need to add additional models. Furthermore, depending on the queries that we need to write, we may need to add more fields to the models (but not necessarily to the tables themselves).

The main example I've seen of this so far is in adding ForeignKey fields in order to work with Django's high level abstraction of table joins. You can see how this is done within the `SearchResult` model with the `web_page_version` ForeignKey field. In particular, I expect we'll need to make a number of modifications to the models as they currently stand in order to support the complicated query for getting the `results_with_code` value for a specific package.

Each model has an embedded `class Meta` in order to explicitly tell it which table in `fetcher` to use; otherwise, it will prepend the application name to the table (e.g. `tutorons_webpagecontent`) and try to access it, which causes an error.

I've included the StackOverflow post you linked to me previously down below under Useful Links and Resources.

## Complete the queries for the other data we want to show
Based on our previous discussion of what we want to include in a package tutoron, we currently are only showing the package name, description, URL, how long it has been documented (`documented_since`), how quickly GitHub issues are responded to (`response_time`), how quickly GitHub issues are resolved (`resolution_time`), and the number of questions on StackOverflow (`num_questions`). In addition to these, we also want to show `results_with_code` from a Google search.

### Results with code
We looked at your code on `Package-Community` and came up with an equivalent SQL query that should get the same result. This SQL query can be found at the top of `example.sql`. It still needs to be translated into Django, which might turn out to be rather involved.

As a reference, the SQL query on the bottom is for retrieving the `documented_since` value for a package. The equivalent Django code can be found in `explain.py` in the function `get_documented_since()`.

## Check that the multi-database setup is actually working
In `settings/dev.py`, I changed the `DATABASES` setting by overriding the one defined in `settings/defaults.py`. The new setting specifies two different databases: the first one is the `default` database and is used for querying the `fetcher` database; the second one is called the `logging` database and is used for logging. In my development so far, I log in using `reader` for the `default` database.

In `tutorons/common/dblogger.py`, call `using('logging')` on the `QuerySet` when dealing with the database in order to make the query write to the correct database.

### Accessing the database
In `settings/defaults.py`, I define a global variable `PASSWORD_FILE` that goes to `/etc/django/password.key`, which is meant to be used to access `fetcher`. In `settings/dev.py`, update the `DATABASES` setting to whichever user you want to use. I currently have it set to `reader` and thus have `reader`'s password stored in `/etc/django/password.key`.

## Useful Links and Resources
[Django: Aggregation](https://docs.djangoproject.com/en/1.9/topics/db/aggregation/)
[Django: Executing Queries](https://docs.djangoproject.com/en/1.9/topics/db/queries/)
[StackOverflow: Performing "Joins"](http://stackoverflow.com/questions/31735717/join-and-query-django-models-on-non-primary-key-relationship#answer-31735867)
