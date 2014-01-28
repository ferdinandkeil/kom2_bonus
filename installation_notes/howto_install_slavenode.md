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
wget https://www.dropbox.com/s/31i5s1pe0mekac4/yasputin_conf.json
# now edit the config file according to your needs
nano yasputin_conf.json
# to autostart the script the file /etc/rc.local has to be changed
sudo nano /etc/rc.local
	...
	(cd /home/pi/yasputin/ && python yasputin.py > /dev/null) &

	exit 0
~~~~~~~~~~~~~~~


Finish
------

The installation is now finished. Please make sure the Plugwise stick is connected to the Raspberry Pi and the Circle+ is plugged to an outlet. You can now restart the slave node and watch the data being uploaded on your master node.

~~~~~~~~bash
sudo reboot
~~~~~~~~~~~~