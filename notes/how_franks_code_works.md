% How Frank's code works
% Ferdinand Keil (ferdinandkeil@googlemail.com)
% 12.11.2013

General structure
=================

The code consists of two projects:

* smtk-rasppi: this containts the code that communicates with the sensor.
* smtk: this is the "pretty" web-interface that presents the collected data to the user. Also containts code related to data retrieval and storage.

In the following the general code structure will be outlined by going through the source code files. Files with a numbered entry get called directly, ones with letters get imported and are libraries of some kind. Striked out entries are dead ends and not used any more.

1. `smtk-rasppi/plugwise/plugwise.py` Communication with the Plugwise USB stick.
	a. `smtk/TraceStore/plugwise_importer.py` Pipeline based implementation for data import.
	b. `smtk-rasppi/plugwise/CrcMoose` CRC implementation.
	c. `serial` Python serial module.
	d. ~~`multiprocessing` Module to spawn processes, used for threading.~~
	e. `subprocess` Python process management module, used to create threads.
2. `smtk/TraceStore/plugwise_importer.py` Pipeline based implementation for data import.
	a. `models Trace, Sensor, OnCycle` Django data models. Used to retrieve and save data.
	b. `mosquitto` MQTT library. Used to make the data accessible via MQTT data streams.
	c. `OnCycleSerializer` Serializer for the OnCycle model. Based on Django's serializer API.


Conclusion so far
=================

* The code lacks proper documentation (comments).
* There are lots of dead ends, unused code fragments and even obsolete files.
* Many things get done in an overly complicated way:
	* The (unnecessary) use of MQTT.
	* The pipeline implementation of `plugwise_importer.py`.
	* Serializers, JSON data, SQlite, ...
	* The use of threading and subprocesses.

I could go on and on, but that gets us nowhere. To me it looks like advanced concepts have been introduced to the codebase before the basic functionality was stable.