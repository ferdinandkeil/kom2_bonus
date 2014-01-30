How-to Install a Slave Node
===========================

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


Install python-plugwise
-----------------------

The upload script relies on python-plugwise by Sven Petai. The following commands will install all dependencies for the script.

~~~~~~~~~~bash
sudo apt-get install mercurial python-setuptools python-requests
hg clone https://bitbucket.org/hadara/python-plugwise
cd python-plugwise
sudo python setup.py install
~~~~~~~~~~~~~~~


Install YASPUtin
----------------

YASPUtin is the script we wrote to retrieve and upload the sensor readings. It is configured through the file yasputin_conf.json. An example config file is supplied, but has to be changed according to your local configuration.

~~~~~~~~~~bash
cd
mkdir yasputin
cd yasputin
wget https://raw.github.com/ferdinandkeil/kom2_bonus/master/yasputin.py
wget https://raw.github.com/ferdinandkeil/kom2_bonus/master/yasputin.sh
wget https://www.dropbox.com/s/31i5s1pe0mekac4/yasputin_conf.json
# now edit the config file according to your needs
# to get an API-key you have register an account in EmonCMS and then
# go to Input -> Input API help
nano yasputin_conf.json
# to autostart the script we will add it as a service
chmod 755 yasputin.py
sudo cp yasputin.sh /etc/init.d/
sudo chmod 755 /etc/init.d/yasputin.sh
sudo update-rc.d yasputin.sh defaults
~~~~~~~~~~~~~~~

You can now start and stop the script using the following command:

~~~~~~~~~~bash
sudo /etc/init.d/yasputin.sh start|stop
~~~~~~~~~~~~~~~


Finish
------

The installation is now finished. Please make sure the Plugwise stick is connected to the Raspberry Pi and the Circle+ is plugged to an outlet. You can now restart the slave node and watch the data being uploaded in EmonCMS.

~~~~~~~~bash
sudo reboot
~~~~~~~~~~~~

> *Note:*
> If you did not install the USB-stick and Circle+ correctly, the data upload script will not start at boot. There will be no error message.
> The same is true for errors in the configuration file. So if the data upload does not work, check the API-key and MAC adresses you entered.
> To check if the script is running enter `sudo /etc/init.d/yasputin.sh status`.