What makes a beautiful street, or a pleasant neighborhood? Maybe that's hard to
define, but can you tell a beautiful place from somewhere that’s not so hot?

Beautiful Streets is a project from
`OpenPlans <http://openplans.org/civicworks>`_. It’s an experiment: we’re
trying out a different way to evaluate places, called pairwise surveys, as
popularized by the fantastic `All Our Ideas <http://AllOurIdeas>`_. We’re also
testing out some neat interface ideas, and learning about the use of Street
View in evaluating places for urban planning projects.

With your help, we’ll compare 200 randomly-selected streets in Philly and ask
which one in each pair is more beautiful.  We expect this experiment will
produce some neat data, which you’ll be able to download here soon.

Try it out, and let us know what you think via
`@OpenPlans <http://twitter.com/openplans>`_ or
`here <http://openplans.org/contact>`_.

Installation
============

Development
-----------

For local development, from the command line, install the requirements::

    $ pip install -r requirements.txt

Fill in the settings::

    $ # From street_score/project/settings/ ...
    $ cp local.py.template local.py
    $ <editor> local.py

Initialize the database::

    $ # From street_score/ ...
    $ python manage.py syncdb --all  # Create a superuser too

Start the server::

    $ python manage.py runserver

Deployment
----------

Deployment to DotCloud and Heroku are straightforward.  First, follow the
respective platform's instructions for setting up the project (all of the
required) files should already be available in the repository).

Add the following environment variables to the system::

    STREETSCORE_DB_NAME
    STREETSCORE_DB_USER
    STREETSCORE_DB_PASS
    STREETSCORE_DB_HOST
    STREETSCORE_DB_PORT

On Heroku you would use ``heroku config:add STREETSCORE_DB_...=...``, and on
DotCloud, ``dotcloud var set <application> STREETSCORE_DB_...=...``.  For other
services, refer to the documentation.

Initializing Data
=================

Before you can run surveys, you need points and a question in the database. You
can add places one at a time or in bulk. In your browser, go to the admin page
for Places (e.g.: http://localhost:8000/admin/project/place/ ). In the top right
of the page there are buttons for adding data.

The application currently has support for one question at a time. To set the
question, browse to the admin for Criteria  (e.g.:
http://localhost:8000/admin/project/criterion/ ). By default the model will
expect something to finish the statement "Which street is more _____?".  To
change the format of the prompt, you will have to edit the `index.html`
template.

Now you should be able to start submitting surveys!

Site Settings
=============

Through the admin interface, you can set the title of the site, the Google
analytics key, and the AddThis credentials so that visitors can easily share
the site.
