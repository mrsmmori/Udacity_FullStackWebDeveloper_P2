Udacity_FullStackWebDeveloper_P2
====

# Overview
This program was built for Udacity Full Stack Web Developer / Project 2.
The objective of this practice project is to build a web application in vagrant.

<a href="https://docs.google.com/document/d/e/2PACX-1vT7XPf0O3oLCACjKEaRVc_Z-nNoG6_ssRoo_Mai5Ce6qFK_v7PpR1lxmudIOqzKo2asKOc89WC-qpfG/pub?embedded=true">Item Catalog: Getting Started</a>

# Description
- **app.py** to run catalog app
- **database.py** to build database layout
- **schema.sql** to define database layout and input some entries

# Usage

- Login vagrant
``` bash 
vagrant@vagrant:/vagrant/catalog
(2.7.12) $ vagrant up
(2.7.12) $ vagrant ssh
vagrant@vagrant:~$ cd /vagrant/catalog
vagrant@vagrant:/vagrant/catalog
```

- build database layout
``` python
vagrant@vagrant:/vagrant/catalog$ flask init-db
Initialized the database.
```

- run app.py
``` python
vagrant@vagrant:/vagrant/catalog$ python app.py
```

# Author

[mrsmmori](https://github.com/mrsmmori)
