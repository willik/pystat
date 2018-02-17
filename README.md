Pystat is a multi threaded thermostat written in Python.
Functionality is implemented with seperate threads, which use threadsafe utility
classes to communicate.

Screen shots are avaiable on Imgur (http://imgur.com/a/7vkZO)

This project is inspired by the Rubustat software
(https://github.com/wywin/Rubustat) created by Wyatt Winters and for my hardware
I followed the specifications detailed in Nich Fugal's blog post
(http://makeatronics.blogspot.com/2013/04/raspberry-pi-thermostat-hookups.html)

Depends upon Flask for the web interface and whatever libraries are needed for
the device in use. I use and have implemented controls for a Raspberry Pi with
RPi.GPIO, however adding support for another device is as simple as implementing
a new GPIOManager class and swapping it in.

Added a database component utilizing sqlite3, which logs the time, the indoor,
outdoor (if available) and target temperatures, the target mode and what
components are currently running.