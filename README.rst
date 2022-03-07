sde.videorent
=============

Implementation of simple video rental usecase based on plone 4.3.20


Installation
============

Prerequisites
-------------

You need the python2.7 virtualenv command under the alias ``virtualenv-2.7``

If you already have a 2.7 virtualenv, in a terminal do::

  sudo ln -s /path-to-python2.7-virtualenv/bin/virtualenv /usr/local/bin/virtualenv-2.7

to create the alias.
And skip this section.

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


Deployment
----------

Clone this git project. In a terminal do::

  cd ~
  git clone https://github.com/sdelcourt/sde.videorent.git
  cd sde.videorent
  make

We use buildout to deploy plone and its dependencies. The first run should take some time, grab a cup of your favourite hot drink meanwhile ;) .
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
