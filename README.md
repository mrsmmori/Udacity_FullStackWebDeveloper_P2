Udacity_FullStackWebDeveloper_P2 / Item Catalog App
====

# Overview
This program was built for Udacity Full Stack Web Developer / Project 2.
The objective of this practice project is to build a mock web application in vagrant. Below are project descriptions:

<a href="https://docs.google.com/document/d/e/2PACX-1vT7XPf0O3oLCACjKEaRVc_Z-nNoG6_ssRoo_Mai5Ce6qFK_v7PpR1lxmudIOqzKo2asKOc89WC-qpfG/pub?embedded=true">Item Catalog: Getting Started</a>


<a href="https://review.udacity.com/#!/rubrics/2008/view">Item Catalog: Rubrics</a>

# Codes
- **app.py** to run catalog app
- **models.py** to define database layout
- **config.py** to define app configuration
- **settings.py** to define flask settings

# Usage

- Login vagrant
``` bash 
(2.7.12) $ vagrant up
(2.7.12) $ vagrant ssh
vagrant@vagrant:~$ cd /vagrant/catalog
vagrant@vagrant:/vagrant/catalog
```

- build database layout and input sample data
``` python
vagrant@vagrant:/vagrant/catalog$ flask initdb
Initialized the database.
```

- run app.py
``` python
vagrant@vagrant:/vagrant/catalog$ python app.py
```

- Open <a href="localhost:8000">localhost:8000</a> in browser.


# Authentication
Page implements Google authentication & authorization service.


# Author

[mrsmmori](https://github.com/mrsmmori)
