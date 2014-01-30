How-to Install the Master Node
==============================

Install Hamachi
---------------

Hamachi is the VPN software used to connect the different nodes. The most up-to-date Debian package supplied by Logmein unfortunately does not work on the Raspberry Pi, so the one supplied below has to be taken.

~~~~~~~~~bash
sudo apt-get update # always a good idea
sudo apt-get install lsb-core
wget https://www.dropbox.com/s/wj64tjiu0qu380u/logmein-hamachi_2.1.0.86-1_armel.deb
sudo dpkg -i --force-depends --force-architecture logmein-hamachi_2.1.0.86-1_armel.deb
~~~~~~~~~~

Now that Hamachi is installed it still has to be connected to a network. The network can be created using the Logmein web-interface. After the commands shown below have been executed the new node has to be approved through the web-interface.

~~~~~~~~~bash
sudo hamachi login
sudo hamachi set-nick [nick] # can be chosen freely
# enter the e-mail address used for your Logmein account
sudo hamachi attach [email-address]
# enter the network-id and password you chose in the web-interface
sudo hamachi do-join [network-id]
~~~~~~~~~~~~~~~~~


Install MySQL
-------------

First we set-up MySQL, the database system used by EmonCMS. It is available via apt-get.

~~~~~bash
sudo apt-get install mysql-server mysql-client
# you'll have to choose a root password for MySQL, make sure to write it down
mysql -u root -p # now we create the database and a user
	> CREATE DATABASE emoncms;
	> USE mysql;
	> GRANT ALL PRIVILEGES ON emoncms.* TO 'emoncms'@'%' IDENTIFIED BY 
	> '9UldLC3JDjmLDO' WITH GRANT OPTION;
	> quit
~~~~~~~~~~~~~~~~~~~


Install nginx and PHP
---------------------

We are using nginx instead of Apache 2, as it is better suited to be run on a constrained system like the Raspberry Pi.

~~~~~~~~bash
sudo apt-get install nginx php5-fpm php5-mysql php5-curl php5-mcrypt
	php-pear php5-dev build-essential
sudo mkdir /var/www
sudo chown www-data:www-data /var/www
wget https://www.dropbox.com/s/qcd4nt05u7xm9sj/nginx_sites-available_default
sudo cp nginx_sites-available_default /etc/nginx/sites-available/default
sudo /etc/init.d/nginx reload
~~~~~~~~~~~~~~~~~


Install Redis
-------------

Redis is an in-memory database and is used by EmonCMS since version 7.

~~~~~~~bash
sudo apt-get install redis-server
~~~~~~~~~~~~~~~~~~~~~~~~~

The PHP module for Redis is not available through apt-get, however it is easy to compile it.

~~~~~~~~~~~bash
sudo pear channel-discover pear.swiftmailer.org
sudo pecl install channel://pecl.php.net/dio-0.0.6 redis swift/swift
# the following cmds tell PHP to load the modules you just compiled
sudo sh -c 'echo "extension=dio.so" > /etc/php5/cli/conf.d/20-dio.ini'
sudo sh -c 'echo "extension=dio.so" > /etc/php5/fpm/conf.d/20-dio.ini'
sudo sh -c 'echo "extension=redis.so" > /etc/php5/cli/conf.d/20-redis.ini'
sudo sh -c 'echo "extension=redis.so" > /etc/php5/fpm/conf.d/20-redis.ini'
sudo /etc/init.d/php5-fpm reload
~~~~~~~~~~~~~~~~~~


Compile and Install Timestore
-----------------------------

EmonCMS uses Mike Stirling's timestore database to store the sensor data. It is available through apt-get on all system, so here a the steps necessary to compile it from source.

~~~~~~~~~bash
sudo apt-get install pkg-config libmicrohttpd-dev autoconf automake git-core
git clone https://github.com/mikestir/timestore.git
	# this clones the timestore source
cd timestore
autoreconf -i
./configure
make all
sudo make install
~~~~~~~~~~~~~~~~~

The timestore binary is now installed, but there are still some tasks left.

~~~~~~~~~bash
sudo mkdir /var/lib/timestore
sudo adduser timestore
sudo chown timestore:timestore /var/lib/timestore
wget https://www.dropbox.com/s/beuqij7dfhnvpd8/init.d_timestore
sudo cp init.d_timestore /etc/init.d/timestore
sudo chmod 755 /etc/init.d/timestore
sudo update-rc.d timestore defaults
sudo /etc/init.d/timestore restart
cat /var/lib/timestore/adminkey.txt 
	# note the admin key, you will need it later
~~~~~~~~~~~~~~~~~~~~~~


Download and Setup EmonCMS
--------------------------

All that is left is downloading and configuring EmonCMS.

~~~~~~~~~~bash
cd /var/www
sudo git clone git://github.com/emoncms/emoncms.git
sudo chown -R www-data:www-data emoncms
cd emoncms
sudo mv default.settings.php settings.php
sudo nano settings.php 
	# here you have to enter the MySQL login credentials and the admin key
~~~~~~~~~~~~~~~~~~~


Finish
------

You can now point your browser to the IP of your device and start using EmonCMS.