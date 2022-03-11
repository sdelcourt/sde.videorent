sde.videorent
=============

Implementation of simple video rental usecase based on plone 4.3.20

Sections
========

- `Installation`_
- `Use`_
- `Thoughts`_


Installation
============

Prerequisites
-------------

You may need to install following libraries::

  apt-get install build-essential
  apt-get install libreadline5-dev
  apt-get install zlib1g-dev (support zlib)
  apt-get install libjpeg62-dev
  apt-get install libpq-dev

You need a python2.7 virtualenv command under the alias ``virtualenv-2.7``

If you already have a 2.7 virtualenv, in a terminal do::

  sudo ln -s /path-to-python2.7-virtualenv/bin/virtualenv /usr/local/bin/virtualenv-2.7

to create the alias .
Skip the rest of this section and directly go to `Install`_.

Install a new python 2.7 that will be used for our virtualenv. Open a terminal::

  cd ~
  wget http://www.python.org/ftp/python/2.7.16/Python-2.7.16.tgz
  tar xvzf Python-2.7.16.tgz
  cd Python-2.7.16
  ./configure --prefix=~/python2716
  make
  make install

Install pip::

  cd ../python2716
  wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
  bin/python2.7 get-pip.py

Install virtualenv::

  bin/pip install virtualenv

Create the alias::

  sudo ln -s ~/python2716/bin/virtualenv /usr/local/bin/virtualenv-2.7

Close the the terminal and open it again. If you type virtualenv and then push tab you should see ``virtualenv-2.7`` in the commands list.


Install
-------

Clone this git project. In a terminal do::

  cd ~
  git clone https://github.com/sdelcourt/sde.videorent.git
  cd sde.videorent
  make

We use buildout to deploy plone and its dependencies. The first run should take some time so grab a cup of your favourite hot drink meanwhile ;) .
If everything goes well, it will end the installation by running the server. You should see something like::

  2022-03-07 06:07:28 INFO ZServer HTTP server started at Mon Mar  7 06:07:28 2022
  Hostname: 0.0.0.0
  Port: 8081
  2022-03-07 06:07:28 WARNING Products.PDBDebugMode

  Debug-Mode enabled!

  This will result in a pdb when a exception happens.
  Turn off debug mode or remove Products.PDBDebugMode to disable.

  See https://pypi.python.org/pypi/Products.PDBDebugMode

  2022-03-07 06:07:30 INFO Plone OpenID system packages not installed, OpenID support not available
  2022-03-07 06:07:30 WARNING plone.behavior Specifying 'for' in behavior 'Related items' if no 'factory' is given has no effect and is superfluous.
  2022-03-07 06:07:33 INFO Zope Ready to handle requests


You can then open the url ``http://localhost:8081/`` in firefox or chrome.
Push on the button "Créer un nouveau site plone".
Login as admin/admin.
Leave the default "identifiant" to Plone and change "Titre" with "VidéoRent"
In the "modules" section, check the box "VidéoRent démo".
Finally, push on "Créer le site plone" at the bottom for form.

You will end up on the front page of the videorent app.
You can now disconnect (right top corner) and reconnect with the user/password manager/manager to start using the app.

For the next use, all you have to do is to go to ``~/sde.videorent``, call ``make`` again (or ``bin/instance fg``) and go to ``http://localhost:8081/Plone``.


Use
===

Run the instance
------------------

Start the instance with::

   cd~/sde.videorent
   bin/instance fg

and go to ``http://localhost:8081/Plone``. Login with manager/manager


Tests
-----

Run the unittests with::

   bin/tests

Test coverage with::

   bin/createcoverage

Restapi
-------

The sde.videorent.restapi will extend the existing plone restapi with two custom endpoints.

POST @rental::

   import requests

   url = 'http://localhost:8081/Plone/rentals/@rental'
   headers = {'Accept': 'application/json','content-type': 'application/json','authorization': 'Basic YWRtaW46YWRtaW4='}
   body = """{
       "customer": "95a5d330c7744e3b828c9e5739413923",
        "rented":[
            {"video_copy": "862a923a5af2473b8ff74def29a334f9", "duration": 5},
            {"video_copy": "5fa5b52964bd4279b6959cfdcfa83df2", "duration": 5}
        ]
   }"""

   req = requests.post(url, headers=headers, data=body)

   rint(req.status_code)
   print(req.headers)
   print(req.text)

Input: a dict with the Customer UID and a list rented with each rented VideoCopy and the rent duration.

Returns: the created Rental object json

It also update the Customer with the Rental total bonus points.

PATCH @rented::

  import requests

  url = 'http://localhost:8081/Plone/rentals/@rented'
  headers = {'Accept': 'application/json','content-type': 'application/json','authorization': 'Basic bWFuYWdlcjptYW5hZ2Vy'}
  body = """["862a923a5af2473b8ff74def29a334f9"]"""

  req = requests.patch(url, headers=headers, data=body)

  print(req.status_code)
  print(req.headers)
        print(req.text)

Input: a list with the VideoCopies UIDs returned.

Returns: update all the Rentals where these videos were in status "not returned"

return a dict with two keys:

- "rentals" contains the updated rentals
- "late_fees" contains the late fees info all the late videocopies

To retrieve the customer UIDs and the videocopies UID we can use the default plone restapi GET @search endpoints

Customer GET @search::

   import requests

   url = 'http://localhost:8081/Plone/@search?portal_type=Customer&metadata_fields=UID'
   headers = {'Accept': 'application/json','authorization': 'Basic bWFuYWdlcjptYW5hZ2Vy'}

   req = requests.get(url, headers=headers)
  
   print(req.status_code)
   print(req.headers)
   print(req.text)


VideoCopy GET @search::

   import requests

   url = 'http://localhost:8081/Plone/@search?portal_type=VideoCopy&metadata_fields=UID'
   headers = {'Accept': 'application/json','authorization': 'Basic bWFuYWdlcjptYW5hZ2Vy'}

   req = requests.get(url, headers=headers)

   print(req.status_code)
   print(req.headers)
   print(req.text)


Thoughts
========

Why Plone ?
-----------
Because Plone is my work framework, its use greatly improved my productivity for this exercise. It also allowed me to transfer the business logic of the endpoints to the python classes of the content types I created. It also allowed me to provides forms and views to explore and vizualise the objects manipulated by the restapi endpoints. Fastapi would have been a more suitable choice for simplicity reasons.

Design & plan
-------------

After considering the problem description, I thought it would be best to separate the "film" as an abstract concept from its physical support (DVD, VHS) which is rented.

The solution will use 4 objects:

- Customer: a person signaletic + an attribute "bonus points".
- Film: a generic film description + an attribute "release type" (new, old, regular).
- VideoCopy : the physical support of the film, different VideoCopies can refers to the same film. The video copy has a unique reference to identify the physical object (barcode or QR code).
- The rental: represents a rent of several VideoCopies (for different rent durations) from a Customer at a given "start date". The rental should be able to compute the rental price, keep track of which VideoCopy has been returned or not, compute the late delays by comparing the rental date to today's date and compute the late fees of each copy that has not been returned.

At the first save of a rental, an event will update the customer bonus points.

Each object types are grouped in 4 individual folders the site root.

With this design, we should be able to solve the three main problems:

- Have an inventory of films (the Film folder and/or the VideoCopy folder).
- Calculate the price of rentals.
- Keep track of the Customer bonus points.

I also want to have an automated setup of test objects to use for a demo profile and for the unittest.
